from flask import Flask, render_template,request,redirect,url_for 
from bson import ObjectId 
from pymongo import MongoClient
import os
import datetime

app = Flask(__name__)
title = "REMINDER"
heading = "HEY!YOUR REMINDER HERE!!"

client = MongoClient("mongodb://soumya123:password123@ds155292.mlab.com:55292/soumya")
db = client['soumya']



todos = db.todo 



@app.route("/list")
def lists ():
	
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)




@app.route("/tlist")
def tlists ():
        todos_l = todos.find({"date": datetime.datetime.utcnow().strftime("%d/%m/%Y")})
        a3="active"
        return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)



@app.route("/")

@app.route("/Create")
def tasks ():
	
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	'''pr=request.values.get("pr")
	todoas_1=todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})'''
	todoas_1=todos.insert({ "name":name, "desc":desc, "date":date})
	return redirect("/list")

                

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	'''pr=request.values.get("pr")'''
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date }})
	return redirect("/")

if __name__ == "__main__":

    app.run()
