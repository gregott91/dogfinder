var timeouts = {};

function changeStatus(element) {
    var status = $(element).data('status')
    status = status + 1

    if (status == 3) {
        status = -1
    }

    updateStatusStyle(element, status)

    var id = $(element).data('id')
    clearTimeout(timeouts[id])
    timeouts[id] = setTimeout(function() {
        $.ajax({
            method: "POST",
            url: "/petstatus/",
            data: { id: $(element).data('id'), status: status }
        });
    }, 1000);
}

function updateStatusStyle(element, status) {
    var parent = $(element).parent()
    switch(status) {
        case -1:
            $(parent).removeClass('unstable_status')
            $(parent).addClass('bad_status')
            break;
        case 0:
            $(parent).removeClass('bad_status')
            $(parent).addClass('neutral_status')
            break;
        case 1:
            $(parent).removeClass('neutral_status')
            $(parent).addClass('good_status')
            break;
        case 2:
            $(parent).removeClass('good_status')
            $(parent).addClass('unstable_status')
            break;
    }

    $(element).data('status', status)
}

function sortStatus(element) {
    sortColumn(element, getCellStatus)
}

function sortAge(element) {
    sortColumn(element, getCellAge)
}

function sortWeight(element) {
    sortColumn(element, getCellWeight)
}

function sortColumn(element, valueFunc) {
    var table = $('table')
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(element).index(), valueFunc))
    element.asc = !element.asc
    if (!element.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
}

function comparer(index, valueFunc) {
    return function(a, b) {
        var valA = valueFunc(a, index), valB = valueFunc(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}

function getCellValue(row, index) { 
    return $(row).children('td').eq(index).text() 
}

function getCellAge(row, index) {
    var text = $(row).children('td').eq(index).text().trim()
    var splits = text.split(" ")
    if (splits[1] == "months") {
        return splits[0]/12
    }
    return splits[0]
}

function getCellWeight(row, index) {
    var text = $(row).children('td').eq(index).text().trim()
    var splits = text.split(" ")
    return splits[0]
}

function getCellStatus(row, index) {
    var status = $(row).children('td').eq(index).data("status")
    return status
}