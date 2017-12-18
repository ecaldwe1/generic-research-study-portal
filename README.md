# Generic Portal

#### Deployment Notes

Installing Gentelella Theme with Bower

    cd tesserae/static/  
    bower install gentelella --save
    bower install highcharts --save
    
Disable PNotify

Open `static/bower_components/gentelella/build/js/custom.js`

Comment out lines 1843 -> 1863 (try searching for "new PNotify")   
** These are what cause the "PNotify" example to show up on all pages (annoying!!)


Please consult the Wiki for further information about the components of the portal.