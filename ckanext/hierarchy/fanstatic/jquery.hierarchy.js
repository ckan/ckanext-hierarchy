"use strict";

(function (jQuery) {

    jQuery.fn.hierarchy = function() {
      $('ul.hierarchy-tree li:last-child').addClass('last');
      return this;
    };


})(this.jQuery);

