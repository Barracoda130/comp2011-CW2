// Function to live search through the table
// Only uses the first element of each line as the search term
jQuery(document).ready(function($) { 
    
    $('.items-table tr:not(:first-child)').each(function() { 
        if ($(this).children()[0].textContent == "")
        {
            $(this).attr('search-data', $(this).children()[1].textContent.toLowerCase()); 
        } else {
            $(this).attr('search-data', $(this).children()[0].textContent.toLowerCase()); 
        }
        
    }); 
        
    $('.searchbox').on('keyup', function() { 
        var searchTerm = $(this).val().toLowerCase(); 
    
        $('.items-table tr:not(:first-child)').each(function() { 
            if (searchTerm == "") {
                $(this).show();
            }
            else if ($(this).filter('[search-data *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) { 
                $(this).show(); 
            } else { 
                $(this).hide(); 
            } 
        }); 
    }); 
}); 