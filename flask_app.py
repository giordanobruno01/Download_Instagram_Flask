from flask import Flask, request, url_for, redirect, render_template, send_file, flash
import instaloader
import shutil
import os
import datetime

from instaloader import *
app = Flask(__name__)
app.secret_key = "hellome"
if __name__ == "__main__":

    app.run(debug=True)
    # app.run(debug=True ,port=8080,use_reloader=False) 

instaL = instaloader.Instaloader()


def deletezip():
    try:
        for i in os.listdir("."):
            if i.endswith(".zip"):
                os.remove(i)
    except:
        pass


@app.route("/", methods=["POST", "GET"])
def logInsta():

    if (request.method == "POST"):

        usern = request.form.get("username").strip()
        # opt = request.form.get("opt")
        if (usern == ""):
            return render_template("index.html", name="Provide a username")
        # passw = request.form.get("password").strip()

        deletezip()

        try:
            opt = request.form.get("opt")
            if (opt == "stories"):
                # instaL.login(user = usern, passwd=passw)
                # instaL.download_stories(userids = [instaL.check_profile_id(usern)])
                instaL.download_storyitem()
            elif (opt == "profile"):
                
                 
                try:
                    instaL.download_profile(usern, profile_pic_only=True, download_stories=True)
                except:
                    try:
                        shutil.make_archive(base_name=usern, format="zip", root_dir=usern)
                    except:
                        return render_template("index.html", name=str(usern + " Try inside zip creator " + opt))
                    return render_template("index.html", name=str(usern + " Try inside profile " + opt))
                

            elif (opt == "reels"):

                instaL.download_videos()
                shutil.make_archive(
                    base_name=usern, format="zip", root_dir=usern)

            elif (opt == "hashtag"):
                hashtag = request.form.get("extra")
                amount = int(request.form.get("amount"))

                instaL.download_hashtag(hashtag, max_count=amount)
                shutil.make_archive(base_name=hashtag,
                                    format="zip", root_dir=str("#"+hashtag))
                try:
                    shutil.rmtree(str("#"+hashtag))
                except:
                    pass
                return send_file(str(hashtag+".zip"), as_attachment=True)

            elif (opt == "highlights"):
                instaL.download_highlights()
                shutil.make_archive(
                    base_name=usern, format="zip", root_dir=usern)

            elif (opt == "post"):

                prof = Profile.from_username(instaL.context, usern)

                post = prof.get_posts()

                for i in post:
                    instaL.download_post(i, target=usern)

                return send_file(shutil.make_archive(base_name=usern, format="zip", root_dir=usern), as_attachment=True)
                # instaL.download_post(target="https://www.instagram.com/p/Cwr2kd0tl2q/?utm_source=ig_web_button_share_sheet")

            elif (opt == "pictures"):

                instaL.download_pictures()
                shutil.make_archive(
                    base_name=usern, format="zip", root_dir=usern)

            elif (opt == "igtv"):

                instaL.download_igtv()
                shutil.make_archive(
                    base_name=usern, format="zip", root_dir=usern)

            elif (opt == "test"):
                startdate = request.form.get("startdate").split("-")
                enddate = request.form.get("startdate").split("-")
                f = startdate.split()[0]
                instaL.download_profile(usern, post_filter=lambda post: (post.date_utc >= datetime.datetime(int(startdate[0]), int(
                    startdate[1]), int(startdate[2])) and post.date_utc <= datetime.datetime(int(enddate[0]), int(enddate[1]), int(enddate[2]))))
                # shutil.make_archive(base_name=usern, format="zip", root_dir=usern)

        except:

            return render_template("index.html", name=str(usern + " is a private account"))

        shutil.make_archive(base_name=usern, format="zip", root_dir=usern)
        try:
            shutil.rmtree(usern)
        except:
            pass

        # instaL.download_feed_posts(max_count=2)

        return send_file(str(usern+".zip"), as_attachment=True)
    else:
        return render_template("index.html")

# python3 -m venv auth
# source auth/bin/activate
# pip3 install gunicorn
# pip3 install requirements.txt
# export FLASK_APP=Unfollower_Instagram_Flask
# FLASK_APP="flask_app.py"
# export FLASK_DEBUG=1
# gunicorn --bind 0.0.0.0:5000 app:app --daemon
# pkill gunicorn
# python3 flask_app.py