//ripped this code from
//https://codepen.io/orist/pen/bVmzoK

function makeSortable(){
  $(function() {
    $("#sortable tbody").sortable({
        update: function(event, ui) {
        reorderTasks()
},
      cursor: "move",
      placeholder: "sortable-placeholder",
      helper: function(e, tr)
      {
        var $originals = tr.children();
        var $helper = tr.clone();
        $helper.children().each(function(index)
        {
        // Set helper cell sizes to match the original sizes
        $(this).width($originals.eq(index).width());

        });
        return $helper;
      }
    }).disableSelection();
  });
  }