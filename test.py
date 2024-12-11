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
    return pymysql.connect(host='sql12.freesqldatabase.com', user='sql12749753', password='a52CtDKya1', database='sql12749753')

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
        approved_reports = cursor.fetchall()
        app.logger.info(f"Approved Reports: {approved_reports}")
        
        # Fetch all declined reports from the bin table
        cursor.execute("SELECT * FROM bin WHERE userid = %s", (userid,))
        declined_reports = cursor.fetchall()
        app.logger.info(f"Declined Reports: {declined_reports}")
        
        # Fetch all pending reports from the report_temp table
        cursor.execute("SELECT * FROM report_temp WHERE userid = %s", (userid,))
        pending_reports = cursor.fetchall()
        app.logger.info(f"Pending Reports: {pending_reports}")
        
        if not pending_reports:
            app.logger.warning("No pending reports found for the current user.")
        
    except Exception as e:
        flash(f"Error fetching reports: {str(e)}", "error")
        app.logger.error(f"Error fetching reports: {str(e)}")
        approved_reports = []
        declined_reports = []
        pending_reports = []
    finally:
        db.close()
    
    # Render the template with all three tables
    return render_template(
        'my_reports.html', 
        approved_reports=approved_reports, 
        declined_reports=declined_reports,
        pending_reports=pending_reports
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
        
        # Updated query to fetch multiple sites, gears, hours, and landings
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
                rt.price1,
                rt.price2,
                rt.price3,
                rt.price4,
                rt.price5,
                s1.name AS site1_name,
                s2.name AS site2_name,
                s3.name AS site3_name,
                s4.name AS site4_name,
                s5.name AS site5_name,
                g1.name AS gear1_name,
                g2.name AS gear2_name,
                g3.name AS gear3_name,
                g4.name AS gear4_name,
                g5.name AS gear5_name,
                rt.hours1,
                rt.hours2,
                rt.hours3,
                rt.hours4,
                rt.hours5,
                l1.name AS landing1_name,
                l2.name AS landing2_name,
                l3.name AS landing3_name,
                l4.name AS landing4_name,
                l5.name AS landing5_name
            FROM report_temp rt
            LEFT JOIN catch c1 ON rt.catch1 = c1.catchid
            LEFT JOIN catch c2 ON rt.catch2 = c2.catchid
            LEFT JOIN catch c3 ON rt.catch3 = c3.catchid
            LEFT JOIN catch c4 ON rt.catch4 = c4.catchid
            LEFT JOIN catch c5 ON rt.catch5 = c5.catchid
            LEFT JOIN site s1 ON rt.site1 = s1.siteid
            LEFT JOIN site s2 ON rt.site2 = s2.siteid
            LEFT JOIN site s3 ON rt.site3 = s3.siteid
            LEFT JOIN site s4 ON rt.site4 = s4.siteid
            LEFT JOIN site s5 ON rt.site5 = s5.siteid
            LEFT JOIN gear g1 ON rt.gear1 = g1.gearid
            LEFT JOIN gear g2 ON rt.gear2 = g2.gearid
            LEFT JOIN gear g3 ON rt.gear3 = g3.gearid
            LEFT JOIN gear g4 ON rt.gear4 = g4.gearid
            LEFT JOIN gear g5 ON rt.gear5 = g5.gearid
            LEFT JOIN landing l1 ON rt.landing1 = l1.landid
            LEFT JOIN landing l2 ON rt.landing2 = l2.landid
            LEFT JOIN landing l3 ON rt.landing3 = l3.landid
            LEFT JOIN landing l4 ON rt.landing4 = l4.landid
            LEFT JOIN landing l5 ON rt.landing5 = l5.landid
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
                # Prepare the INSERT query for the updated `report` table
                sql_insert = """
                    INSERT INTO report (userid, name, vessel, frequent, date, 
                                        catch1, catch2, catch3, catch4, catch5, 
                                        volume1, volume2, volume3, volume4, volume5, 
                                        price1, price2, price3, price4, price5,
                                        site1, site2, site3, site4, site5,
                                        gear1, gear2, gear3, gear4, gear5,
                                        hours1, hours2, hours3, hours4, hours5,
                                        landing1, landing2, landing3, landing4, landing5,
                                        tempid)
                    VALUES (%s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s)
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
                    report['price1'], report['price2'], report['price3'], 
                    report['price4'], report['price5'],  # Ensure these are int or float
                    report['site1'], report['site2'], report['site3'], 
                    report['site4'], report['site5'],  # Ensure these are int
                    report['gear1'], report['gear2'], report['gear3'], 
                    report['gear4'], report['gear5'],  # Ensure these are int
                    report['hours1'], report['hours2'], report['hours3'], 
                    report['hours4'], report['hours5'],  # Ensure these are int
                    report['landing1'], report['landing2'], report['landing3'], 
                    report['landing4'], report['landing5'],  # Ensure these are int
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

# Pending Users Page
@app.route('/pending_users')
def pending_users():
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        # Fetch all pending users
        cursor.execute("SELECT userid, username, password, vessel_name, reg_number, contact FROM user_temp")
        users = cursor.fetchall()
        db.close()
        
        return render_template('pending_users.html', users=users)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


# Approving a pending user
@app.route('/approve_user/<int:userid>', methods=['POST'])
def approve_user(userid):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            # Fetch the user from `user_temp`
            cursor.execute("SELECT * FROM user_temp WHERE userid = %s", (userid,))
            user = cursor.fetchone()

            if user:
                # Insert the user into the `user` table
                sql_insert_user = """
                    INSERT INTO user (userid, username, password, vessel_name, reg_number, contact) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert_user, (
                    user['userid'], user['username'], user['password'],
                    user['vessel_name'], user['reg_number'], user['contact']
                ))

                # Delete the user from `user_temp`
                cursor.execute("DELETE FROM user_temp WHERE userid = %s", (userid,))
                db.commit()

                flash("User approved and moved to the user table successfully!", "success")
            else:
                flash("User not found!", "error")

        except Exception as e:
            db.rollback()
            app.logger.error(f"Error approving user ID {userid}: {str(e)}")
            flash(f"Error while approving user: {str(e)}", "error")

        finally:
            db.close()

        return redirect(url_for("pending_users"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))


# Deleting a pending user
@app.route('/delete_user/<int:userid>', methods=['POST'])
def delete_user(userid):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            # Delete the user from the `user_temp` table
            cursor.execute("DELETE FROM user_temp WHERE userid = %s", (userid,))
            db.commit()

            flash("User deleted successfully!", "success")
        except Exception as e:
            db.rollback()
            app.logger.error(f"Error deleting user ID {userid}: {str(e)}")
            flash(f"Error while deleting user: {str(e)}", "error")

        finally:
            db.close()

        return redirect(url_for("pending_users"))
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
            cursor.execute("INSERT INTO user_temp (username, password,vessel_name, reg_number,contact) VALUES (%s, %s,%s, %s, %s)", (username, password, vessel_name, reg_number, contact))
            db.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('register'))
        finally:
            db.close()
    return render_template('register.html')

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = validate(request.form['username'])
        password = validate(request.form['password'])

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('admin_register'))
        finally:
            db.close()
    return render_template('admin_register.html')

# User report submission
@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'id' not in session:
        flash("You need to be logged in to submit a report.", "error")
        return redirect(url_for('login'))
    
    userid = session['id']

    try:
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Fetching dropdown data
        cursor.execute("SELECT catchid, name FROM catch")
        catch = cursor.fetchall()
        cursor.execute("SELECT gearid, name FROM gear")
        gear = cursor.fetchall()
        cursor.execute("SELECT landid, name FROM landing")
        landing = cursor.fetchall()
        cursor.execute("SELECT siteid, name FROM site")
        site = cursor.fetchall()

        if request.method == 'POST':
            # Function to handle adding new items to respective tables
            def add_if_not_exists(cursor, table, column, value):
                if not value:
                    return None
                
                # Check if the value already exists
                cursor.execute(f"SELECT {column}id FROM {table} WHERE name = %s", (value,))
                existing = cursor.fetchone()
                
                if existing:
                    return existing[f'{column}id']
                
                # If not exists, insert new item
                cursor.execute(f"INSERT INTO {table} (name) VALUES (%s)", (value,))
                return cursor.lastrowid

            # Add new items for catches, sites, landings, and gears
            new_catches = [
                add_if_not_exists(cursor, 'catch', 'catch', request.form.get(f"catch{i}")) 
                for i in range(1, 6)
            ]

            new_sites = [
                add_if_not_exists(cursor, 'site', 'site', request.form.get(f"site{i}")) 
                for i in range(1, 6)
            ]

            new_landings = [
                add_if_not_exists(cursor, 'landing', 'land', request.form.get(f"landing{i}")) 
                for i in range(1, 6)
            ]

            new_gears = [
                add_if_not_exists(cursor, 'gear', 'gear', request.form.get(f"gear{i}")) 
                for i in range(1, 6)
            ]

            # Rest of the code remains the same as in the previous implementation
            sql = """INSERT INTO report_temp (
                        userid, name, vessel, frequent, date, 
                        catch1, catch2, catch3, catch4, catch5, 
                        volume1, volume2, volume3, volume4, volume5, 
                        site1, site2, site3, site4, site5,
                        gear1, gear2, gear3, gear4, gear5,
                        hours1, hours2, hours3, hours4, hours5,
                        landing1, landing2, landing3, landing4, landing5,
                        price1, price2, price3, price4, price5) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s)"""
            values = (
                userid,
                request.form.get("name"), request.form.get("vessel"),
                request.form.get("frequent"), request.form.get("date"),
                *new_catches, 
                request.form.get("volume1"), request.form.get("volume2"),
                request.form.get("volume3"), request.form.get("volume4"),
                request.form.get("volume5"), 
                *new_sites,
                *new_gears,
                request.form.get("hours1"), request.form.get("hours2"),
                request.form.get("hours3"), request.form.get("hours4"),
                request.form.get("hours5"), 
                *new_landings,
                request.form.get("price1"), request.form.get("price2"),
                request.form.get("price3"), request.form.get("price4"),
                request.form.get("price5"),
            )

            cursor.execute(sql, values)
            db.commit()
            flash("Report submitted successfully!", "success")
            return redirect(url_for('my_reports'))
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        flash("An error occurred while processing your report.", "error")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    
    return render_template('report.html', catch=catch, gear=gear, landing=landing, site=site)


# Admin dashboard
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'id' in session and session['role'] == 'admin':
        try:
            db = connect_db()
            cursor = db.cursor(pymysql.cursors.DictCursor)

            # Get the selected year from the form or default to 2022
            selected_year = request.form.get('year', 2022)
            years = [2020, 2021, 2022, 2023, 2024, 2025]

            # Query for yearly ranking
            cursor.execute(f"""
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
                     AND YEAR(r.date) = %s
                GROUP BY species_name
                ORDER BY total_volume DESC;
            """, (selected_year,))
            species_ranking = cursor.fetchall()

            # Query for monthly species ranking
            cursor.execute("""
                SELECT 
                    main.period,
                    main.species_name,
                    main.total_volume
                FROM (
                    SELECT 
                        CASE 
                            WHEN EXTRACT(MONTH FROM r.date) IS NULL THEN 'Year' 
                            ELSE MONTHNAME(r.date) 
                        END AS period,
                        CASE 
                            WHEN r.catch1 BETWEEN 2 AND 42 THEN c1.name
                            WHEN r.catch2 BETWEEN 2 AND 42 THEN c2.name
                            WHEN r.catch3 BETWEEN 2 AND 42 THEN c3.name
                            WHEN r.catch4 BETWEEN 2 AND 42 THEN c4.name
                            WHEN r.catch5 BETWEEN 2 AND 42 THEN c5.name
                        END AS species_name,
                        SUM(
                            CASE WHEN r.catch1 BETWEEN 2 AND 42 THEN COALESCE(r.volume1, 0) ELSE 0 END +
                            CASE WHEN r.catch2 BETWEEN 2 AND 42 THEN COALESCE(r.volume2, 0) ELSE 0 END +
                            CASE WHEN r.catch3 BETWEEN 2 AND 42 THEN COALESCE(r.volume3, 0) ELSE 0 END +
                            CASE WHEN r.catch4 BETWEEN 2 AND 42 THEN COALESCE(r.volume4, 0) ELSE 0 END +
                            CASE WHEN r.catch5 BETWEEN 2 AND 42 THEN COALESCE(r.volume5, 0) ELSE 0 END
                        ) AS total_volume
                    FROM report r
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
                                WHEN EXTRACT(MONTH FROM r2.date) IS NULL THEN 'Year' 
                                ELSE MONTHNAME(r2.date) 
                            END AS period,
                            CASE 
                                WHEN r2.catch1 BETWEEN 2 AND 42 THEN c1.name
                                WHEN r2.catch2 BETWEEN 2 AND 42 THEN c2.name
                                WHEN r2.catch3 BETWEEN 2 AND 42 THEN c3.name
                                WHEN r2.catch4 BETWEEN 2 AND 42 THEN c4.name
                                WHEN r2.catch5 BETWEEN 2 AND 42 THEN c5.name
                            END AS species_name,
                            SUM(
                                CASE WHEN r2.catch1 BETWEEN 2 AND 42 THEN COALESCE(r2.volume1, 0) ELSE 0 END +
                                CASE WHEN r2.catch2 BETWEEN 2 AND 42 THEN COALESCE(r2.volume2, 0) ELSE 0 END +
                                CASE WHEN r2.catch3 BETWEEN 2 AND 42 THEN COALESCE(r2.volume3, 0) ELSE 0 END +
                                CASE WHEN r2.catch4 BETWEEN 2 AND 42 THEN COALESCE(r2.volume4, 0) ELSE 0 END +
                                CASE WHEN r2.catch5 BETWEEN 2 AND 42 THEN COALESCE(r2.volume5, 0) ELSE 0 END
                            ) AS total_volume
                        FROM report r2
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

            return render_template(
                'admin_dashboard.html',
                species_ranking=species_ranking,
                species_rankings=species_rankings,
                selected_year=int(selected_year),
                years=years
            )
        except Exception as e:
            print("Error:", e)
            flash("There was an error loading the dashboard.", "error")
            return redirect(url_for("admin_login"))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("admin_login"))

#Route for Data Visualization
@app.route('/admin/visualization_page', methods=['GET', 'POST'])
def visualization_page():
    species_list = []  # For dropdowns
    plot_url = None
    no_data_message = None

    # Fetch species list for dropdowns
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

    # Generate the overview graph (default view)
    if request.method == 'GET':
        try:
            connection = connect_db()
            query_overview = """
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
                cursor.execute(query_overview)
                result_overview = cursor.fetchall()

            df_overview = pd.DataFrame(result_overview)
            if not df_overview.empty:
                # Plot the overview graph
                plt.figure(figsize=(12, 8))
                species_names = df_overview['species_name'].unique()
                for species_name, group_data in df_overview.groupby('species_name'):
                    plt.plot(
                        group_data['month'],
                        group_data['frequency'],
                        marker='o',
                        linestyle='-',
                        label=f"{species_name}"
                    )
                plt.title('Overview: Monthly Catch Frequency')
                plt.xlabel('Month')
                plt.ylabel('Frequency')
                plt.xticks(range(1, 13))
                plt.legend(title='Species', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(True)
                plt.tight_layout()

                # Save the plot as base64
                img = io.BytesIO()
                plt.savefig(img, format='png')
                plt.close()
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
        except Exception as e:
            print(f"Error generating the overview graph: {e}")
        finally:
            if connection:
                connection.close()

    # Handle form submission (POST method)
    if request.method == 'POST':
        selected_species = request.form.get('species')
        selected_year = request.form.get('year')
        graph_type = request.form.get('graph_type')  # Either 'volume' or 'frequency'
        selected_species_name = next(
            (species['name'] for species in species_list if str(species['catchid']) == selected_species),
            "Unknown Species"
        )

        if graph_type == 'volume':
            # Generate the volume graph
            try:
                connection = connect_db()
                query_volume = """
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
                    cursor.execute(query_volume, (selected_species,) * 6 + (selected_year,))
                    result_volume = cursor.fetchall()

                df_volume = pd.DataFrame(result_volume)
                if df_volume.empty:
                    no_data_message = f"No data available for {selected_species_name} in {selected_year}."
                else:
                    # Plot the volume graph
                    plt.figure(figsize=(12, 8))
                    plt.plot(
                        df_volume['month'],
                        df_volume['total_volume'],
                        marker='o',
                        linestyle='-',
                        color='blue',
                        linewidth=2,
                        label=f"{selected_species_name} ({selected_year})"
                    )
                    plt.title(f'{selected_species_name} - Monthly Catch Volume ({selected_year})')
                    plt.xlabel('Month')
                    plt.ylabel('Volume')
                    plt.xticks(range(1, 13))
                    plt.legend(loc='upper right')
                    plt.grid(True)
                    plt.tight_layout()

                    # Save the plot as base64
                    img = io.BytesIO()
                    plt.savefig(img, format='png')
                    plt.close()
                    img.seek(0)
                    plot_url = base64.b64encode(img.getvalue()).decode()

            except Exception as e:
                print(f"Error generating volume graph: {e}")
            finally:
                if connection:
                    connection.close()

        elif graph_type == 'frequency':
            # Generate the frequency graph
            try:
                connection = connect_db()
                query_frequency = """
                SELECT 
                    EXTRACT(MONTH FROM r.date) AS month,
                    COUNT(
                        CASE 
                            WHEN r.catch1 = %s THEN 1 
                            WHEN r.catch2 = %s THEN 1 
                            WHEN r.catch3 = %s THEN 1 
                            WHEN r.catch4 = %s THEN 1 
                            WHEN r.catch5 = %s THEN 1 
                        END
                    ) AS frequency
                FROM report r
                WHERE %s IN (r.catch1, r.catch2, r.catch3, r.catch4, r.catch5)
                AND YEAR(r.date) = %s
                GROUP BY month
                ORDER BY month;
                """
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(query_frequency, (selected_species,) * 6 + (selected_year,))
                    result_frequency = cursor.fetchall()

                df_frequency = pd.DataFrame(result_frequency)
                if df_frequency.empty:
                    no_data_message = f"No data available for {selected_species_name} in {selected_year}."
                else:
                    # Plot the frequency graph
                    plt.figure(figsize=(12, 8))
                    plt.plot(
                        df_frequency['month'],
                        df_frequency['frequency'],
                        marker='o',
                        linestyle='-',
                        color='red',
                        linewidth=2,
                        label=f"{selected_species_name} ({selected_year})"
                    )
                    plt.title(f'{selected_species_name} - Monthly Catch Frequency ({selected_year})')
                    plt.xlabel('Month')
                    plt.ylabel('Frequency')
                    plt.xticks(range(1, 13))
                    plt.legend(loc='upper right')
                    plt.grid(True)
                    plt.tight_layout()

                    # Save the plot as base64
                    img = io.BytesIO()
                    plt.savefig(img, format='png')
                    plt.close()
                    img.seek(0)
                    plot_url = base64.b64encode(img.getvalue()).decode()

            except Exception as e:
                print(f"Error generating frequency graph: {e}")
            finally:
                if connection:
                    connection.close()

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

@app.route('/admin/userlist')
def userlist():
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user")
        user = cursor.fetchall()
        db.close()
        return render_template('userlist.html', user=user)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))

#Export to CSV
@app.route('/admin/export_reports')
def export_reports():
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Updated SQL query with new fields
        cursor.execute("""
            SELECT 
                r.reportid, r.name, r.vessel, r.frequent, 
                DATE_FORMAT(r.date, '%Y-%m-%d') AS date,  -- Format date as YYYY-MM-DD
                c1.name AS catch1_name, c2.name AS catch2_name, 
                c3.name AS catch3_name, c4.name AS catch4_name, c5.name AS catch5_name,
                r.volume1, r.volume2, r.volume3, r.volume4, r.volume5,
                r.price1, r.price2, r.price3, r.price4, r.price5,
                s1.name AS site1_name, s2.name AS site2_name, 
                s3.name AS site3_name, s4.name AS site4_name, s5.name AS site5_name,
                g1.name AS gear1_name, g2.name AS gear2_name, 
                g3.name AS gear3_name, g4.name AS gear4_name, g5.name AS gear5_name,
                r.hours1, r.hours2, r.hours3, r.hours4, r.hours5,
                l1.name AS landing1_name, l2.name AS landing2_name, 
                l3.name AS landing3_name, l4.name AS landing4_name, l5.name AS landing5_name
            FROM report r
            LEFT JOIN catch c1 ON r.catch1 = c1.catchid
            LEFT JOIN catch c2 ON r.catch2 = c2.catchid
            LEFT JOIN catch c3 ON r.catch3 = c3.catchid
            LEFT JOIN catch c4 ON r.catch4 = c4.catchid
            LEFT JOIN catch c5 ON r.catch5 = c5.catchid
            LEFT JOIN site s1 ON r.site1 = s1.siteid
            LEFT JOIN site s2 ON r.site2 = s2.siteid
            LEFT JOIN site s3 ON r.site3 = s3.siteid
            LEFT JOIN site s4 ON r.site4 = s4.siteid
            LEFT JOIN site s5 ON r.site5 = s5.siteid
            LEFT JOIN gear g1 ON r.gear1 = g1.gearid
            LEFT JOIN gear g2 ON r.gear2 = g2.gearid
            LEFT JOIN gear g3 ON r.gear3 = g3.gearid
            LEFT JOIN gear g4 ON r.gear4 = g4.gearid
            LEFT JOIN gear g5 ON r.gear5 = g5.gearid
            LEFT JOIN landing l1 ON r.landing1 = l1.landid
            LEFT JOIN landing l2 ON r.landing2 = l2.landid
            LEFT JOIN landing l3 ON r.landing3 = l3.landid
            LEFT JOIN landing l4 ON r.landing4 = l4.landid
            LEFT JOIN landing l5 ON r.landing5 = l5.landid
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
                "Price1", "Price2", "Price3", "Price4", "Price5",
                "Site1", "Site2", "Site3", "Site4", "Site5",
                "Gear1", "Gear2", "Gear3", "Gear4", "Gear5",
                "Hours1", "Hours2", "Hours3", "Hours4", "Hours5",
                "Landing1", "Landing2", "Landing3", "Landing4", "Landing5"
            ]
            yield ','.join(header) + '\n'

            for report in reports:
                row = [
                    report["reportid"], report["name"], report["vessel"], report["frequent"], report["date"],
                    report["catch1_name"], report["catch2_name"], report["catch3_name"], 
                    report["catch4_name"], report["catch5_name"],
                    report["volume1"], report["volume2"], report["volume3"], 
                    report["volume4"], report["volume5"],
                    report["price1"], report["price2"], report["price3"], 
                    report["price4"], report["price5"],
                    report["site1_name"], report["site2_name"], report["site3_name"], 
                    report["site4_name"], report["site5_name"],
                    report["gear1_name"], report["gear2_name"], report["gear3_name"], 
                    report["gear4_name"], report["gear5_name"],
                    report["hours1"], report["hours2"], report["hours3"], 
                    report["hours4"], report["hours5"],
                    report["landing1_name"], report["landing2_name"], report["landing3_name"], 
                    report["landing4_name"], report["landing5_name"]
                ]
                # Convert all row values to strings and join with commas
                yield ','.join(map(str, row)) + '\n'

        return Response(generate(), mimetype='text/csv',
                        headers={"Content-Disposition": "attachment;filename=reports.csv"})
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for("login"))

#Route for export to pdf    
@app.route('/admin/export_pdf/<int:report_id>')
def export_pdf(report_id):
    if 'id' in session and session['role'] == 'admin':
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # SQL query to fetch the report and catch details
        query = """
            SELECT 
                r.reportid, r.name, r.vessel, r.frequent, 
                DATE_FORMAT(r.date, '%%Y-%%m-%%d') AS date,
                c1.name AS catch1_name, r.volume1, r.price1, r.hours1, g1.name AS gear1_name, s1.name AS site1_name, l1.name AS landing1_name,
                c2.name AS catch2_name, r.volume2, r.price2, r.hours2, g2.name AS gear2_name, s2.name AS site2_name, l2.name AS landing2_name,
                c3.name AS catch3_name, r.volume3, r.price3, r.hours3, g3.name AS gear3_name, s3.name AS site3_name, l3.name AS landing3_name,
                c4.name AS catch4_name, r.volume4, r.price4, r.hours4, g4.name AS gear4_name, s4.name AS site4_name, l4.name AS landing4_name,
                c5.name AS catch5_name, r.volume5, r.price5, r.hours5, g5.name AS gear5_name, s5.name AS site5_name, l5.name AS landing5_name
            FROM report r
            LEFT JOIN catch c1 ON r.catch1 = c1.catchid
            LEFT JOIN catch c2 ON r.catch2 = c2.catchid
            LEFT JOIN catch c3 ON r.catch3 = c3.catchid
            LEFT JOIN catch c4 ON r.catch4 = c4.catchid
            LEFT JOIN catch c5 ON r.catch5 = c5.catchid
            LEFT JOIN site s1 ON r.site1 = s1.siteid
            LEFT JOIN site s2 ON r.site2 = s2.siteid
            LEFT JOIN site s3 ON r.site3 = s3.siteid
            LEFT JOIN site s4 ON r.site4 = s4.siteid
            LEFT JOIN site s5 ON r.site5 = s5.siteid
            LEFT JOIN gear g1 ON r.gear1 = g1.gearid
            LEFT JOIN gear g2 ON r.gear2 = g2.gearid
            LEFT JOIN gear g3 ON r.gear3 = g3.gearid
            LEFT JOIN gear g4 ON r.gear4 = g4.gearid
            LEFT JOIN gear g5 ON r.gear5 = g5.gearid
            LEFT JOIN landing l1 ON r.landing1 = l1.landid
            LEFT JOIN landing l2 ON r.landing2 = l2.landid
            LEFT JOIN landing l3 ON r.landing3 = l3.landid
            LEFT JOIN landing l4 ON r.landing4 = l4.landid
            LEFT JOIN landing l5 ON r.landing5 = l5.landid
            WHERE r.reportid = %s
        """
        cursor.execute(query, (report_id,))
        report = cursor.fetchone()
        db.close()

        if not report:
            flash("Report not found.", "error")
            return redirect(url_for('view_reports'))

        # Generate PDF in landscape orientation
        pdf = FPDF(orientation='L', unit='mm', format='A4')  # Landscape
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Report Details', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)

        # Add general report details
        general_details = [
            ("Report ID", report["reportid"]),
            ("Name", report["name"]),
            ("Vessel", report["vessel"]),
            ("Frequent", report["frequent"]),
            ("Date", report["date"]),
        ]
        for label, value in general_details:
            pdf.cell(0, 10, f"{label}: {value}", 0, 1)

        # Add a table for catches
        pdf.cell(0, 10, '', 0, 1)  # Add space before table
        pdf.set_font('Arial', 'B', 12)

        # Table header with custom color
        pdf.set_fill_color(76, 175, 80)  # Header background color (#4CAF50)
        pdf.set_text_color(255, 255, 255)  # White text
        pdf.cell(40, 10, "Catch", 1, 0, 'C', True)
        pdf.cell(30, 10, "Volume (kg)", 1, 0, 'C', True)
        pdf.cell(30, 10, "Price/Kilo", 1, 0, 'C', True)
        pdf.cell(40, 10, "Fishing Duration", 1, 0, 'C', True)
        pdf.cell(40, 10, "Fishing Gear", 1, 0, 'C', True)
        pdf.cell(50, 10, "Fishing Site", 1, 0, 'C', True)
        pdf.cell(50, 10, "Landing Site", 1, 1, 'C', True)

        # Reset text color for table data
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 12)

        # Add rows for each catch
        for i in range(1, 6):  # Loop through catches 1 to 5
            catch_name = report.get(f"catch{i}_name", "N/A")
            volume = report.get(f"volume{i}", "N/A")
            price = report.get(f"price{i}", "N/A")
            duration = report.get(f"hours{i}", "N/A")
            gear = report.get(f"gear{i}_name", "N/A")
            site = report.get(f"site{i}_name", "N/A")
            landing = report.get(f"landing{i}_name", "N/A")

            pdf.cell(40, 10, catch_name, 1)
            pdf.cell(30, 10, str(volume), 1)
            pdf.cell(30, 10, f"{price}", 1)
            pdf.cell(40, 10, f"{duration} hrs", 1)
            pdf.cell(40, 10, gear, 1)
            pdf.cell(50, 10, site, 1)
            pdf.cell(50, 10, landing, 1)
            pdf.ln()

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