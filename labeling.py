from flask import render_template, request, redirect, url_for, session, flash
from helpers import get_next_unlabeled_file, save_labels
import json

def label_data():
    if not session.get('logged_in'):
        return redirect(url_for('login_route'))

    list_of_views = ['Parasternal long axis (PLAX)', 'Parasternal short axis(PSAX)', 'Apical Four Chamber(A4C)', 'Apical three chamber (A3C)', 'Apical two chamber(A2C)', 'Suprasternal(SSN)', 'Subcostal', 'Doppler']
    list_of_colours = ['Colour', 'No Colour']
    list_of_thickness_state = ['Thick', 'Not Thick', 'Not Applicable']
    list_of_conditions = ['Mitral Valve Regurgitation', 'Aortic Valve Regurgitation', 'Tricuspid Valve Regurgitation', 'Pulmonary Valve Regurgitation', 'Aortic Valve Stenosis', 'Mitral Valve Stenosis', 'Tricuspid Valve Stenosis', 'Pulmonary Valve Stenosis', 'Mitral Valve Prolapse', 'Not Applicable']
    list_of_severities = ['Normal', 'Borderline rhd', 'Definite rhd', 'Not Applicable']


    if request.method == 'POST':
        # Save labels to MySQL database
        file_path = request.form.get('filename')
        conditions = request.form.getlist('conditions')  # This will now get all checked conditions
        
        # if not conditions:
        #     flash('Please select at least one condition', 'error')
        #     return redirect(url_for('label_route'))
    
        labels = {
            'view': request.form.get('view'),
            'colour': request.form.get('colour'),
            'thickness_state': request.form.get('thickness_state'),
            'thickness_comment': request.form.get('thickness_comment'),
            'conditions': request.form.getlist('conditions'),
            'conditions_comment': request.form.get('conditions_comment'),
            'echo_quality_comment': request.form.get('echo_quality_comment'),
            'severity': request.form.get('severity'),
            'timetaken': request.form.get('timetaken')
        }
        save_labels(file_path, labels)
        # Move to next image/video
        return redirect(url_for('label_route'))

    # Get next unlabeled image/video
    file_path = get_next_unlabeled_file()
    
    
    return render_template('label.html', 
                           file_to_label=file_path,
                           list_of_views=list_of_views,
                           list_of_colours=list_of_colours,
                           list_of_thickness_state=list_of_thickness_state,
                           list_of_conditions=list_of_conditions,
                           list_of_severities=list_of_severities,
                           username=session.get('username'),
                           current_file_index=session.get('labeled_files', 0),
                           total_files=session.get('total_files', 0))