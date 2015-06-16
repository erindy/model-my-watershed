"use strict";

// Cross-site forgery protection
// From https://docs.djangoproject.com/en/dev/ref/contrib/csrf/

var $ = require('jquery');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Source: http://stackoverflow.com/questions/6238351/fastest-way-to-detect-external-urls
var isExternal = (function(){
    var domainRe = /https?:\/\/((?:[\w\d]+\.)+[\w\d]{2,})/i;

    return function(url) {
        function domain(url) {
          var result = domainRe.exec(url) !== null ? domainRe.exec(url)[1] : null;
          return result;
        }

        return domain(location.href) !== domain(url);
    };
})();

exports.jqueryAjaxSetupOptions = {
    beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !isExternal(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
};