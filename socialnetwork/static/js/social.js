function commentReplyToggle(parent_id) {
    console.log(parent_id);

    const row = document.getElementById(parent_id);

    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    }
    else {
        row.classList.add('d-none')
    }
}


function showNotifications() {
    const container = document.getElementById('notification-container')

    if (container.classList.contains('d-none')) {
        container.classList.remove('d-none');
    }
    else {
        container.classList.add('d-none')
    }
}


// using jQuery
function getCookie(name) {
    /**
     * Retrieve the CSRF token from a cookie.
     *
     * @param {string} name - The name of the cookie.
     * @returns {string} The value of the cookie.
     * 
     */
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



/**
 * Removes a notification by sending an HTTP DELETE request.
 *
 * @param {string} removeNotificationURL - The URL to send the DELETE request to.
 * @param {string} redirectURL - The URL to redirect to after successful removal.
 */

function removeNotification(removeNotificationURL, redirectURL) {

    // Retrieve the CSRF token from the cookie.
    var csrftoken = getCookie('csrftoken'); 
    // Create a new XMLHttpRequest object.
    let xmlhttp = new XMLHttpRequest();

    // Set up an event handler to monitor changes in the request's state.
    xmlhttp.onreadystatechange = function() {
        // Check if the request is done.
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            // Check if the response status is 200 (OK).
            if (xmlhttp.status == 200) {
                // Redirect to the specified URL after successful removal.
                window.location.replace(redirectURL);
            }
            else {
                // Display an error alert if the response status is not 200.
                alert('There was an error');
            }
        }
    };

    // Configure the XMLHttpRequest for a DELETE request.
    xmlhttp.open('DELETE', removeNotificationURL, true);
    // Set the 'X-CSRFToken' header with the CSRF token.
    xmlhttp.setRequestHeader('X-CSRFToken', csrftoken);
    // Send the DELETE request.
    xmlhttp.send();
}