$(document).ready(function(){
    $('[data-organization-tree] .js-expand').bind('click', function(){
        // Separate rule for buttons since .show() results in 'block'
        $(this).siblings('.js-collapse.btn').css('display', 'inline-block');
        
        $(this).siblings('.js-collapse, .js-collapsed').show()
        $(this).hide();
    });

    $('[data-organization-tree] .js-collapse').bind('click', function(){
        $(this).hide().siblings('.js-collapsed').hide();
        $(this).siblings('.js-expand').show()
    });

    // Typing in the search box filters the results. Matches and parents of
    // the matches are shown. The match part is highlighted
    $('[data-organization-filter]').bind('keyup cut paste', function(){
        var search_str = $(this).val().toLowerCase();

        if (search_str.length != 0){
            var count = 0;
            $('.js-collapse, .js-expand').hide();
            $('.js-collapsed').show();
            var organizations = $('.organization-list-item');
            organizations.hide();
            var organization_rows = organizations.find('.organization-row');
            
            // Remove previous highlights
            organization_rows.find('a span').removeClass('highlight');
            
            var matching_organization_rows = organization_rows.filter(function(index, organization_row){
                // The organization row also includes the dataset count, which we don't want to include in
                // filtering. Therefore, we get only the link text. It is assumed that there is only one
                // 'a' tag for each organization row
                return organization_row.getElementsByTagName('a')[0].text.toLowerCase().indexOf(search_str) >= 0;
            });
            for(i = 0; i < matching_organization_rows.length; i++){
                // It's necessary to use the 'eq' function here so that the result is still a JQuery element
                var organization_link = matching_organization_rows.eq(i).find('a');
                var text = organization_link.text();
                var str_index = text.toLowerCase().indexOf(search_str);
                organization_link.html(text.substr(0, str_index) + 
                                       '<span class="highlight">' + 
                                       text.substr(str_index, search_str.length) + 
                                       '</span>' + 
                                       text.substr(str_index + search_str.length));
            }
            count = matching_organization_rows.length;
            matching_organization_rows.show();
            matching_organization_rows.parents('.organization-list-item').show()
            // Plus and minus buttons are not visible so empty space is hidden as well
            $('.organization-hierarchy-empty-space').hide();
        }
        else {
            // If search term is empty the changes are reversed
            // and everything is shown normally
            count = $('.organization-list-item').length;
            $('span.highlight').contents().unwrap()
            $('.organization-list-item').show();
            $('.js-collapsed').hide();
            $('.js-expand').show();
            $('.organization-hierarchy-empty-space').show();
        }

        var count_str = $('.search-form h1').text();
        var replaced = count_str.replace(/\d+/g, count);
        $('.search-form h1').text(replaced);
    })
});