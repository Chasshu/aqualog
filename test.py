import base64
import io
from matplotlib import pyplot as plt
import pandas as pd
import pymysql
import csv
from fpdf import FPDF
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for, Response, send_file

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to your secret key

# Database connection
def connect_db():
    return pymysql.connect(host='sql12.freesqldatabase.com', user='sql12747991', password='FGUrVzuy7A', database='sql12747991')

# Function to sanitize input data<input type="password" name="password" placeholder="Password" required>
def validate(data):
    data = data.strip()
    data = data.replace('\\', '')
    data = data.replace('"', '\\"')
    return data

@app.route('/')
def index():
    return render_template('index.html')

# Route for user login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = validate(request.form['username'])
        password = validate(request.form['password'])

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        db.close()

        if result:
            session['id'] = result[0]
            session['username'] = result[1]
            session['role'] = 'user'
            flash("LOGIN SUCCESSFULLY!", "success")
            return redirect(url_for("report"))
        else:
            flash("USER DOESN'T EXIST!", "error")
    return render_template('login.html')

# Route for admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = validate(request.form['username'])
        password = validate(request.form['password'])

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        db.close()

        if result:
            session['id'] = result[0]
            session['username'] = result[1]
            session['role'] = 'admin'
            flash("LOGIN SUCCESSFULLY!", "success")
            return redirect(url_for("sidebar"))
        else:
            flash("ADMIN DOESN'T EXIST!", "error")
    return render_template('admin_login.html')

#sidebar
@app.route('/sidebar')
def sidebar():
    if 'id' not in session:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("login"))
    return render_template('sidebar.html', session=session)

#my reports
@app.route('/my_reports')
def my_reports():
    if 'id' not in session:  # Ensure the user is logged in
        flash("Please login first!", "error")
        return redirect(url_for("login"))
    
    userid = session['id']  # Get the logged-in user's ID
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    
    try:
        # Fetch all approved reports from the report table
        cursor.execute("SELECT * FROM report WHERE userid = %s", (userid,))
        approved_reports = cursor.fetchall()  # Fetch all rows for approved reports
        app.logger.info(f"Approved Reports: {approved_reports}")
        
        # Fetch all declined reports from the bin table
        cursor.execute("SELECT * FROM bin WHERE userid = %s", (userid,))
        declined_reports = cursor.fetchall()  # Fetch all rows for declined reports
        app.logger.info(f"Declined Reports: {declined_reports}")
        
        if not declined_reports:
            app.logger.warning("No declined reports found for the current user.")
        
    except Exception as e:
        flash(f"Error fetching reports: {str(e)}", "error")
        app.logger.error(f"Error fetching reports: {str(e)}")
        approved_reports = []
        declined_reports = []
    finally:
        db.close()
    
    # Render the template with both tables
    return render_template(
        'my_reports.html', 
        approved_reports=approved_reports, 
        declined_reports=declined_reports
    )

# Route for pending reports page
@app.route('/pending')
def pending():
    if 'id' in session:
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM report_temp")  # Fetch only pending reports
        reports = cursor.fetchall()
        db.close()
        return render_template('pending.html', reports=reports)
    else:
        flash("Please login first!", "error")
        return redirect(url_for("login"))
#view report
@app.route('/viewreport/<int:reportid>')
def viewreport(reportid):
    if 'id' in session:
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        # Updated query to fetch names instead of IDs
        cursor.execute("""
            SELECT 
                rt.reportid,
                rt.name AS reporter_name,
                rt.vessel,
                rt.date,
                c1.name AS catch1_name,
                c2.name AS catch2_name,
                c3.name AS catch3_name,
                c4.name AS catch4_name,
                c5.name AS catch5_name,
                rt.volume1,
                rt.volume2,
                rt.volume3,
                rt.volume4,
                rt.volume5,
                s.name AS site_name,
                g.name AS gear_name,
                rt.hours,
                l.name AS landing_name,
                rt.price
            FROM report_temp rt
            LEFT JOIN catch c1 ON rt.catch1 = c1.catchid
            LEFT JOIN catch c2 ON rt.catch2 = c2.catchid
            LEFT JOIN catch c3 ON rt.catch3 = c3.catchid
            LEFT JOIN catch c4 ON rt.catch4 = c4.catchid
            LEFT JOIN catch c5 ON rt.catch5 = c5.catchid
            LEFT JOIN site s ON rt.site = s.siteid
            LEFT JOIN gear g ON rt.gear = g.gearid
            LEFT JOIN landing l ON rt.landing = l.landid
            WHERE rt.reportid = %s
        """, (reportid,))
        
        report = cursor.fetchone()
        db.close()
        
        if report:
            return render_template('viewreport.html', report=report)
        else:
            flash("Report not found!", "error")
            return redirect(url_for("pending"))
    else:
        flash("Please login first!", "error")
        return redirect(url_for("login"))

# Approving a report
@app.route('/approvereport/<int:reportid>')
def approvereport(reportid):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            # Fetch the report from `report_temp` using reportid
            cursor.execute("SELECT * FROM report_temp WHERE reportid = %s", (reportid,))
            report = cursor.fetchone()

            if report:
                # Prepare the INSERT query for the `report` table
                sql_insert = """
                    INSERT INTO report (userid, name, vessel, frequent, date, 
                                        catch1, catch2, catch3, catch4, catch5, 
                                        volume1, volume2, volume3, volume4, volume5, 
                                        site, gear, hours, landing, price, tempid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Create a tuple of values to insert, including `tempid`
                insert_values = (
                    report['userid'],  # Ensure this is int
                    report['name'],    # Ensure this is str
                    report['vessel'],  # Ensure this is str
                    report['frequent'],  # Ensure this is int
                    report['date'],    # Ensure this is a valid date
                    report['catch1'], report['catch2'], report['catch3'], 
                    report['catch4'], report['catch5'],  # Ensure these are int
                    report['volume1'], report['volume2'], report['volume3'], 
                    report['volume4'], report['volume5'],  # Ensure these are int
                    report['site'], report['gear'],  # Ensure these are int
                    report['hours'],  # Ensure this is int
                    report['landing'],  # Ensure this is int
                    report['price'],  # Ensure this is int or float
                    report['reportid']  # This becomes tempid
                )

                # Log the SQL and values for debugging
                app.logger.info("SQL Insert Query: %s", sql_insert)
                app.logger.info("Insert Values: %s", insert_values)

                # Execute the INSERT operation
                cursor.execute(sql_insert, insert_values)

                # Delete the report from `report_temp`
                cursor.execute("DELETE FROM report_temp WHERE reportid = %s", (reportid,))
                db.commit()

                flash("Report approved and moved to the report table successfully!", "success")
            else:
                flash("Report not found!", "error")

        except Exception as e:
            db.rollback()
            # Log the exact error for debugging
            app.logger.error("Error approving report ID %s: %s", reportid, str(e))
            flash(f"Error while approving report: {str(e)}", "error")

        finally:
            cursor.close()
            db.close()

        return redirect(url_for("pending"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


# Deleting a pending report
@app.route('/delete_report/<int:reportid>', methods=['GET', 'POST'])
def delete_report(reportid):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            # Fetch the report from the temporary table
            cursor.execute("SELECT * FROM report_temp WHERE reportid = %s", (reportid,))
            report = cursor.fetchone()
            app.logger.info(f"Fetched report for deletion: {report}")

            if report:
                # Use `userid` from the fetched report
                userid = report['userid']

                # Insert the report into the bin table
                sql_insert_bin = """
                    INSERT INTO bin (id, userid, name, vessel, date, reportid) 
                    VALUES (NULL, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_bin, (
                    userid,  # userid from the report_temp table
                    report['name'],  # name from report_temp
                    report['vessel'],  # vessel from report_temp
                    report['date'],  # date from report_temp
                    reportid  # reportid from report_temp
                ))

                # Delete the report from the report_temp table
                cursor.execute("DELETE FROM report_temp WHERE reportid = %s", (reportid,))
                db.commit()

                flash("Report moved to the trash successfully!", "success")
            else:
                flash("Report not found in the temporary table!", "error")
                app.logger.warning(f"Report ID {reportid} not found in report_temp.")

        except Exception as e:
            db.rollback()
            app.logger.error(f"Error deleting report ID {reportid}: {str(e)}")
            flash(f"Error while deleting report: {str(e)}", "error")

        finally:
            db.close()

        return redirect(url_for("pending"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


#forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        contact = request.form['contact']
        
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        try:
            # Check if the user exists
            cursor.execute(
                "SELECT userid FROM user WHERE reg_number = %s AND contact = %s", 
                (reg_number, contact)
            )
            user = cursor.fetchone()
            
            if user:
                session['userid'] = user['userid']  # Store the user ID in session
                flash("Details verified. Proceed to reset your password.", "success")
                return redirect(url_for('reset_password'))
            else:
                flash("Invalid registration number or contact details.", "error")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
        finally:
            db.close()
    
    return render_template('forgot_password.html')
#reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'userid' not in session:
        flash("Unauthorized access!", "error")
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))
        
        db = connect_db()
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "UPDATE user SET password = %s WHERE userid = %s", 
                (new_password, session['userid'])
            )
            db.commit()
            flash("Password reset successfully. You can now log in.", "success")
            session.pop('userid', None)  # Clear session after success
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "error")
        finally:
            db.close()
    
    return render_template('reset_password.html')


# User logout
@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash("You have been logged out!", "success")
    return redirect(url_for("login"))

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = validate(request.form['username'])
        password = validate(request.form['password'])
        vessel_name = validate(request.form['vessel_name'])
        reg_number = validate(request.form['reg_number'])
        contact = validate(request.form['contact'])
        

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO user (username, password,vessel_name, reg_number,contact) VALUES (%s, %s,%s, %s, %s)", (username, password, vessel_name, reg_number, contact))
            db.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('register'))
        finally:
            db.close()
    return render_template('register.html')

# User report submission
@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'id' not in session:  # Ensure the user is logged in
        flash("You need to be logged in to submit a report.", "error")
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    userid = session['id']  # Retrieve user ID from session

    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Fetching dropdown data
    cursor.execute("SELECT catchid, name FROM catch")  # Fetch catch data
    catch = cursor.fetchall()
    cursor.execute("SELECT gearid, name FROM gear")  # Fetch gear data
    gear = cursor.fetchall()
    cursor.execute("SELECT landid, name FROM landing")  # Fetch landing data
    landing = cursor.fetchall()
    cursor.execute("SELECT siteid, name FROM site")  # Fetch site data
    site = cursor.fetchall()

    if request.method == 'POST':
        try:
            # Prepare the SQL query
            sql = """INSERT INTO report_temp 
                        (`userid`, `name`, `vessel`, `frequent`, `date`, 
                         `catch1`, `catch2`, `catch3`, `catch4`, `catch5`, 
                         `volume1`, `volume2`, `volume3`, `volume4`, `volume5`, 
                         `site`, `gear`, `hours`, `landing`, `price`) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                             %s, %s, %s, %s, %s, %s, %s, %s)"""

            # Bind values from the form
            values = (
                userid,  # User ID from session
                request.form["name"], request.form["vessel"], request.form["frequent"], 
                request.form["date"], request.form["catch1"], request.form["catch2"], 
                request.form["catch3"], request.form["catch4"], request.form["catch5"], 
                request.form["volume1"], request.form["volume2"], request.form["volume3"], 
                request.form["volume4"], request.form["volume5"], request.form["site"], 
                request.form["gear"], request.form["hours"], request.form["landing"], 
                request.form["price"]
            )

            # Log values for debugging
            print("Values to Insert:", values)

            # Execute the query
            cursor.execute(sql, values)
            db.commit()  # Commit the transaction
            
            flash("Report submitted successfully!", "success")
            return redirect(url_for('report'))
        except Exception as e:
            db.rollback()  # Rollback the transaction on error
            flash(f"Error inserting data: {str(e)}", "error")
            print(f"Database Error: {e}")  # Log the error
        finally:
            cursor.close()
            db.close()
    
    return render_template('report.html', catch=catch, gear=gear, landing=landing, site=site)



# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'id' in session and session['role'] == 'admin':
        try:
            db = connect_db()
            cursor = db.cursor(pymysql.cursors.DictCursor)

            # Query to fetch yearly species ranking by total catch volume
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN r.`catch1` BETWEEN 2 AND 42 THEN c1.name
                        WHEN r.`catch2` BETWEEN 2 AND 42 THEN c2.name
                        WHEN r.`catch3` BETWEEN 2 AND 42 THEN c3.name
                        WHEN r.`catch4` BETWEEN 2 AND 42 THEN c4.name
                        WHEN r.`catch5` BETWEEN 2 AND 42 THEN c5.name
                    END AS species_name,
                    SUM(CASE WHEN r.`catch1` BETWEEN 2 AND 42 THEN COALESCE(r.`volume1`, 0) ELSE 0 END) +
                    SUM(CASE WHEN r.`catch2` BETWEEN 2 AND 42 THEN COALESCE(r.`volume2`, 0) ELSE 0 END) +
                    SUM(CASE WHEN r.`catch3` BETWEEN 2 AND 42 THEN COALESCE(r.`volume3`, 0) ELSE 0 END) +
                    SUM(CASE WHEN r.`catch4` BETWEEN 2 AND 42 THEN COALESCE(r.`volume4`, 0) ELSE 0 END) +
                    SUM(CASE WHEN r.`catch5` BETWEEN 2 AND 42 THEN COALESCE(r.`volume5`, 0) ELSE 0 END) AS total_volume
                FROM `report` r
                LEFT JOIN catch c1 ON r.catch1 = c1.catchid
                LEFT JOIN catch c2 ON r.catch2 = c2.catchid
                LEFT JOIN catch c3 ON r.catch3 = c3.catchid
                LEFT JOIN catch c4 ON r.catch4 = c4.catchid
                LEFT JOIN catch c5 ON r.catch5 = c5.catchid
                WHERE 
                    (r.catch1 BETWEEN 2 AND 42 OR 
                     r.catch2 BETWEEN 2 AND 42 OR 
                     r.catch3 BETWEEN 2 AND 42 OR 
                     r.catch4 BETWEEN 2 AND 42 OR 
                     r.catch5 BETWEEN 2 AND 42)
                GROUP BY species_name
                ORDER BY total_volume DESC;
            """)
            species_ranking = cursor.fetchall()

            # Query to fetch monthly species ranking by total catch volume with species name
            cursor.execute("""
                SELECT 
                    main.period,
                    main.species_name,
                    main.total_volume
                FROM (
                    SELECT 
                        CASE 
                            WHEN EXTRACT(MONTH FROM r.`date`) IS NULL THEN 'Year' 
                            ELSE MONTHNAME(r.`date`) 
                        END AS period,
                        CASE 
                            WHEN r.`catch1` BETWEEN 2 AND 42 THEN c1.name
                            WHEN r.`catch2` BETWEEN 2 AND 42 THEN c2.name
                            WHEN r.`catch3` BETWEEN 2 AND 42 THEN c3.name
                            WHEN r.`catch4` BETWEEN 2 AND 42 THEN c4.name
                            WHEN r.`catch5` BETWEEN 2 AND 42 THEN c5.name
                        END AS species_name,
                        SUM(
                            CASE WHEN r.`catch1` BETWEEN 2 AND 42 THEN COALESCE(r.`volume1`, 0) ELSE 0 END +
                            CASE WHEN r.`catch2` BETWEEN 2 AND 42 THEN COALESCE(r.`volume2`, 0) ELSE 0 END +
                            CASE WHEN r.`catch3` BETWEEN 2 AND 42 THEN COALESCE(r.`volume3`, 0) ELSE 0 END +
                            CASE WHEN r.`catch4` BETWEEN 2 AND 42 THEN COALESCE(r.`volume4`, 0) ELSE 0 END +
                            CASE WHEN r.`catch5` BETWEEN 2 AND 42 THEN COALESCE(r.`volume5`, 0) ELSE 0 END
                        ) AS total_volume
                    FROM `report` r
                    LEFT JOIN catch c1 ON r.catch1 = c1.catchid
                    LEFT JOIN catch c2 ON r.catch2 = c2.catchid
                    LEFT JOIN catch c3 ON r.catch3 = c3.catchid
                    LEFT JOIN catch c4 ON r.catch4 = c4.catchid
                    LEFT JOIN catch c5 ON r.catch5 = c5.catchid
                    WHERE 
                        (r.catch1 BETWEEN 2 AND 42 OR 
                         r.catch2 BETWEEN 2 AND 42 OR 
                         r.catch3 BETWEEN 2 AND 42 OR 
                         r.catch4 BETWEEN 2 AND 42 OR 
                         r.catch5 BETWEEN 2 AND 42)
                    GROUP BY period, species_name
                ) AS main
                WHERE main.total_volume = (
                    SELECT MAX(sub.total_volume)
                    FROM (
                        SELECT 
                            CASE 
                                WHEN EXTRACT(MONTH FROM r2.`date`) IS NULL THEN 'Year' 
                                ELSE MONTHNAME(r2.`date`) 
                            END AS period,
                            CASE 
                                WHEN r2.`catch1` BETWEEN 2 AND 42 THEN c1.name
                                WHEN r2.`catch2` BETWEEN 2 AND 42 THEN c2.name
                                WHEN r2.`catch3` BETWEEN 2 AND 42 THEN c3.name
                                WHEN r2.`catch4` BETWEEN 2 AND 42 THEN c4.name
                                WHEN r2.`catch5` BETWEEN 2 AND 42 THEN c5.name
                            END AS species_name,
                            SUM(
                                CASE WHEN r2.`catch1` BETWEEN 2 AND 42 THEN COALESCE(r2.`volume1`, 0) ELSE 0 END +
                                CASE WHEN r2.`catch2` BETWEEN 2 AND 42 THEN COALESCE(r2.`volume2`, 0) ELSE 0 END +
                                CASE WHEN r2.`catch3` BETWEEN 2 AND 42 THEN COALESCE(r2.`volume3`, 0) ELSE 0 END +
                                CASE WHEN r2.`catch4` BETWEEN 2 AND 42 THEN COALESCE(r2.`volume4`, 0) ELSE 0 END +
                                CASE WHEN r2.`catch5` BETWEEN 2 AND 42 THEN COALESCE(r2.`volume5`, 0) ELSE 0 END
                            ) AS total_volume
                        FROM `report` r2
                        LEFT JOIN catch c1 ON r2.catch1 = c1.catchid
                        LEFT JOIN catch c2 ON r2.catch2 = c2.catchid
                        LEFT JOIN catch c3 ON r2.catch3 = c3.catchid
                        LEFT JOIN catch c4 ON r2.catch4 = c4.catchid
                        LEFT JOIN catch c5 ON r2.catch5 = c5.catchid
                        WHERE 
                            (r2.catch1 BETWEEN 2 AND 42 OR 
                             r2.catch2 BETWEEN 2 AND 42 OR 
                             r2.catch3 BETWEEN 2 AND 42 OR 
                             r2.catch4 BETWEEN 2 AND 42 OR 
                             r2.catch5 BETWEEN 2 AND 42)
                        GROUP BY period, species_name
                    ) AS sub
                    WHERE sub.period = main.period
                )
                ORDER BY main.period;
            """)
            species_rankings = cursor.fetchall()

            cursor.close()
            db.close()

            # Pass both rankings to the template
            return render_template('admin_dashboard.html', species_ranking=species_ranking, species_rankings=species_rankings)

        except Exception as e:
            print("Error:", e)
            flash("There was an error loading the dashboard.", "error")
            return redirect(url_for("admin_login"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("admin_login"))



@app.route('/admin/visualization_page', methods=['GET', 'POST'])
def visualization_page():
    species_list = []
    df_default = pd.DataFrame()  # Data for the overview graph
    df_selected = pd.DataFrame()  # Data for the selected species and year
    plot_url = None
    no_data_message = None  # Message for cases with no data

    # Fetch species list for the dropdown
    try:
        connection = connect_db()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT catchid, name FROM catch")
            species_list = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching species list: {e}")
    finally:
        if connection:
            connection.close()

    # Default data for the overview graph
    try:
        connection = connect_db()
        query_default = """
        SELECT 
            s.name AS species_name, 
            EXTRACT(MONTH FROM r.date) AS month, 
            COUNT(
                CASE 
                    WHEN r.catch1 = s.catchid THEN 1 
                    WHEN r.catch2 = s.catchid THEN 1 
                    WHEN r.catch3 = s.catchid THEN 1 
                    WHEN r.catch4 = s.catchid THEN 1 
                    WHEN r.catch5 = s.catchid THEN 1 
                END
            ) AS frequency
        FROM report r
        JOIN catch s 
            ON s.catchid IN (r.catch1, r.catch2, r.catch3, r.catch4, r.catch5)
        WHERE s.catchid != 1
        GROUP BY s.name, EXTRACT(MONTH FROM r.date)
        ORDER BY s.name, month;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query_default)
            result_default = cursor.fetchall()
            df_default = pd.DataFrame(result_default)
    except Exception as e:
        print(f"Error fetching default data: {e}")
    finally:
        if connection:
            connection.close()

    # Fetch data for a selected species and year if form is submitted
    if request.method == 'POST':
        selected_species = request.form.get('species')
        selected_year = request.form.get('year')
        selected_species_name = next(
            (species['name'] for species in species_list if str(species['catchid']) == selected_species),
            "Unknown Species"
        )

        try:
            connection = connect_db()
            query_selected = """
            SELECT 
                EXTRACT(MONTH FROM r.date) AS month,
                SUM(
                    CASE 
                        WHEN r.catch1 = %s THEN r.volume1
                        WHEN r.catch2 = %s THEN r.volume2
                        WHEN r.catch3 = %s THEN r.volume3
                        WHEN r.catch4 = %s THEN r.volume4
                        WHEN r.catch5 = %s THEN r.volume5
                    END
                ) AS total_volume
            FROM report r
            WHERE %s IN (r.catch1, r.catch2, r.catch3, r.catch4, r.catch5)
            AND YEAR(r.date) = %s
            GROUP BY month
            ORDER BY month;
            """
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_selected, (selected_species,) * 6 + (selected_year,))
                result_selected = cursor.fetchall()
                df_selected = pd.DataFrame(result_selected)

            if df_selected.empty:
                no_data_message = f"No data available for {selected_species_name} in {selected_year}."

        except Exception as e:
            print(f"Error fetching selected species and year data: {e}")
        finally:
            if connection:
                connection.close()

    # Create the plot
    try:
        plt.figure(figsize=(12, 8))

        if request.method == 'GET' and not df_default.empty:
            # Overview graph: plot the default frequency data
            for species_name, group_data in df_default.groupby('species_name'):
                plt.plot(
                    group_data['month'],
                    group_data['frequency'],
                    linestyle='--',
                    label=f"{species_name}"
                )
            plt.title('Overview: Monthly Catch Frequency')
            plt.xlabel('Month')
            plt.ylabel('Frequency')
            plt.xticks(range(1, 13))
            plt.legend(title='Species Name', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)
            plt.tight_layout()

        elif request.method == 'POST' and not df_selected.empty:
            # Plot a new graph for the selected species and year (volume)
            plt.plot(
                df_selected['month'],
                df_selected['total_volume'],
                marker='o',
                linestyle='-',
                color='blue',
                linewidth=2,
                label=f"{selected_species_name} (Year {selected_year})"
            )
            plt.title(f'{selected_species_name} - Monthly Catch Volume ({selected_year})')
            plt.xlabel('Month')
            plt.ylabel('Volume')
            plt.xticks(range(1, 13))
            plt.legend(loc='upper right')
            plt.grid(True)
            plt.tight_layout()

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        # Encode the image to base64 to embed in HTML
        plot_url = base64.b64encode(img.getvalue()).decode()
    except Exception as e:
        print(f"Error generating the plot: {e}")

    # Render the template
    return render_template(
        'visualization.html',
        species_list=species_list,
        plot_url=plot_url,
        no_data_message=no_data_message
    )


# Admin geo-tagging page
@app.route('/admin/geo-tagging')
def geo_tagging():
    if 'id' in session and session['role'] == 'admin':
        return render_template('geo_tagging.html')
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("admin_login"))

# Viewing approved reports
@app.route('/admin/view_reports')
def view_reports():
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM report")
        reports = cursor.fetchall()
        db.close()
        return render_template('view_reports.html', reports=reports)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))

@app.route('/admin/export_reports')
def export_reports():
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Updated SQL query with formatted date
        cursor.execute("""
            SELECT 
                r.reportid, r.name, r.vessel, r.frequent, 
                DATE_FORMAT(r.date, '%Y-%m-%d') AS date,  -- Format date as YYYY-MM-DD
                c1.name AS catch1_name, c2.name AS catch2_name, 
                c3.name AS catch3_name, c4.name AS catch4_name, c5.name AS catch5_name,
                r.volume1, r.volume2, r.volume3, r.volume4, r.volume5,
                s.name AS site_name, g.name AS gear_name, r.hours,
                l.name AS landing_name, r.price
            FROM report r
            LEFT JOIN catch c1 ON r.catch1 = c1.catchid
            LEFT JOIN catch c2 ON r.catch2 = c2.catchid
            LEFT JOIN catch c3 ON r.catch3 = c3.catchid
            LEFT JOIN catch c4 ON r.catch4 = c4.catchid
            LEFT JOIN catch c5 ON r.catch5 = c5.catchid
            LEFT JOIN site s ON r.site = s.siteid
            LEFT JOIN gear g ON r.gear = g.gearid
            LEFT JOIN landing l ON r.landing = l.landid
        """)

        reports = cursor.fetchall()
        db.close()

        # Create CSV response
        def generate():
            # Header for the CSV file
            header = [
                "Report ID", "Name", "Vessel", "Frequent", "Date", 
                "Catch1", "Catch2", "Catch3", "Catch4", "Catch5",
                "Volume1", "Volume2", "Volume3", "Volume4", "Volume5",
                "Site", "Gear", "Hours", "Landing", "Price"
            ]
            yield ','.join(header) + '\n'

            for report in reports:
                # Format the date to ensure it's in the correct format
                date = report["date"]  # Already formatted by SQL

                row = [
                    report["reportid"], report["name"], report["vessel"], report["frequent"], date,
                    report["catch1_name"], report["catch2_name"], report["catch3_name"], 
                    report["catch4_name"], report["catch5_name"],
                    report["volume1"], report["volume2"], report["volume3"], 
                    report["volume4"], report["volume5"],
                    report["site_name"], report["gear_name"], report["hours"], 
                    report["landing_name"], report["price"]
                ]
                # Convert all row values to strings and join with commas
                yield ','.join(map(str, row)) + '\n'

        return Response(generate(), mimetype='text/csv',
                        headers={"Content-Disposition": "attachment;filename=reports.csv"})
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))
    
@app.route('/admin/export_pdf/<int:report_id>')
def export_pdf(report_id):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Query to fetch report details
        query = """
            SELECT 
            r.reportid, r.name, r.vessel, r.frequent, 
            DATE_FORMAT(r.date, '%%Y-%%m-%%d') AS date,
            c1.name AS catch1_name, c2.name AS catch2_name, 
            c3.name AS catch3_name, c4.name AS catch4_name, c5.name AS catch5_name,
            r.volume1, r.volume2, r.volume3, r.volume4, r.volume5,
            s.name AS site_name, g.name AS gear_name, r.hours,
            l.name AS landing_name, r.price
            FROM report r
            LEFT JOIN catch c1 ON r.catch1 = c1.catchid
            LEFT JOIN catch c2 ON r.catch2 = c2.catchid
            LEFT JOIN catch c3 ON r.catch3 = c3.catchid
            LEFT JOIN catch c4 ON r.catch4 = c4.catchid
            LEFT JOIN catch c5 ON r.catch5 = c5.catchid
            LEFT JOIN site s ON r.site = s.siteid
            LEFT JOIN gear g ON r.gear = g.gearid
            LEFT JOIN landing l ON r.landing = l.landid
            WHERE r.reportid = %s
        """
        cursor.execute(query, (report_id,))
        report = cursor.fetchone()
        db.close()

        if not report:
            flash("Report not found.", "error")
            return redirect(url_for('view_reports'))

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Report Details', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)

        # General Report Information
        pdf.cell(0, 10, f"Report ID: {report['reportid']}", 0, 1)
        pdf.cell(0, 10, f"Name: {report['name']}", 0, 1)
        pdf.cell(0, 10, f"Vessel: {report['vessel']}", 0, 1)
        pdf.cell(0, 10, f"Date: {report['date']}", 0, 1)
        pdf.cell(0, 10, f"Site: {report['site_name']}", 0, 1)
        pdf.cell(0, 10, f"Gear: {report['gear_name']}", 0, 1)
        pdf.cell(0, 10, f"Landing: {report['landing_name']}", 0, 1)

        # Add Table Header
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(60, 10, 'Catch', 1, 0, 'C')
        pdf.cell(60, 10, 'Volume', 1, 0, 'C')
        pdf.cell(60, 10, 'Price', 1, 1, 'C')

        # Add Table Rows
        pdf.set_font('Arial', '', 12)
        for i in range(1, 6):  # Iterate through Catch1 to Catch5
            catch = report.get(f'catch{i}_name', 'N/A')
            volume = report.get(f'volume{i}', 'N/A')
            price = f"${report['price']:.2f}" if report['price'] else "N/A"

            if catch != 'N/A':  # Add only non-empty catches
                pdf.cell(60, 10, str(catch), 1, 0, 'C')
                pdf.cell(60, 10, str(volume), 1, 0, 'C')
                pdf.cell(60, 10, price, 1, 1, 'C')

        # Ensure the output directory exists
        output_dir = 'generated_reports'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdf_output = os.path.join(output_dir, f'report_{report_id}.pdf')
        pdf.output(pdf_output)

        return send_file(pdf_output, as_attachment=True, download_name=f"report_{report_id}.pdf")
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))

    
if __name__ == '__main__':
    app.run(debug=True)
