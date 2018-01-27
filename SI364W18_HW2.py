## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	albumName = StringField('Enter the name of an album:', validators = [Required()])
	radioButtons = RadioField('How much do you like this album? (1 = low, 3 = high)', choices = [('1', '1'), ('2', '2'), ('3', '3')], validators = [Required()] )
	submit = SubmitField('Click to submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/artistform')
def artistform():
		return render_template('artistform.html')

@app.route('/artistinfo', methods = ('POST', 'GET'))
def artistinfo():
	if request.method == 'GET':
		artist = request.args['artist'] #gets name from initial form

		baseurl = 'https://itunes.apple.com/search?' #sets up search query for itunes api
		param_dict = {'entity': 'song', 'term': artist}
		artist_info = requests.get(baseurl, params = param_dict)
		artist_info = artist_info.json() #converts request object into a dictionary, much easier to iterate thru

	
		return render_template('artist_info.html', objects = artist_info['results']) #returns rendered template with relevant variables


@app.route('/artistlinks')
def specificsong():
	return render_template('artist_links.html') #returns template of artist links


@app.route('/specific/song/<artist_name>')
def specificartist(artist_name):

	baseurl = 'https://itunes.apple.com/search?' #sets up search query for itunes api
	param_dict = {'entity': 'song', 'term': artist_name}
	artist_info = requests.get(baseurl, params = param_dict)
	artist_info = artist_info.json() #converts request object into a dictionary, much easier to iterate thru

	return render_template('specific_artist.html', results = artist_info['results'])

@app.route('/album_entry')
def albumentry():
	form = AlbumEntryForm()
	return render_template('album_entry.html', form = form)

@app.route('/album_result', methods = ('POST', 'GET'))
def album_result():

	if request.method == 'POST':
		
		album_name = request.form['albumName']
		howMuchLike = request.form['radioButtons']		

		return render_template('album_result.html', name = album_name, like = howMuchLike)


@app.route('/user/<name>')
def hello_user(name):
	return '<h1>Hello {0}<h1>'.format(name)


if __name__ == '__main__':
	app.run(use_reloader=True,debug=True)
