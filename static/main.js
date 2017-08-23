$(function() {
    $.showLoading({
        name: 'jump-pulse'
    })

    $(document).keypress(function(e) {
        if ((e.keyCode == 27) && ($('#settings_modal').is(':visible'))) {
            $('#settings_modal').modal('toggle')
        }

        if ((e.keyCode == 115) && (!$('#settings_modal').is(':visible'))) {
            $('#settings_modal').modal('toggle')
        }
    });

    //$("#settings_modal").on('show.bs.modal', function() {});

    if (wallet_id) {
        load_data()
    }

    $("#settings_submit").on('click', function(e) {
        var data = get_form_data($('#settings_form').serializeArray())

        $.ajax({
            url: '/api/wallet/' + wallet_id + '/',
            type: "PUT",
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(result) {
                show_data(result)
                $('#settings_modal').modal('toggle')
            },
            error: function(xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })

        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
});

function get_form_data(data) {
    var unindexed_array = data;
    var indexed_array = {};

    $.map(unindexed_array, function(n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function load_data() {
    $.ajax({
        type: "GET",
        url: "/api/wallet/" + wallet_id + '/',
        success: function(data) {
            show_data(data)
            $.hideLoading()
            setTimeout(load_data, 60000)
        },
        error: function(xhr, resp, text) {
            $.hideLoading()
            if (text === 'UNAUTHORIZED') {
                alert('Unknown Wallet: ' + wallet_id)
            }
        }
    });
}

function show_data(data) {
    $.each(data, function(value, data) {
        $('#' + value).html(data)
    })
    $('#coin_eth_price').html(data['coins_price']['ETH']['price_str'])
    $('#wallet_link').attr('href', window.location.href)

    if (parseFloat(data['profit_p']) < 0) {
        $('.profit_box').css({
            'color': 'red'
        })
    } else {
        $('.profit_box').css({
            'color': 'blue'
        })
    }

    $("#wallets_details tr").remove()
    $.each(data['coins_accounts'], function(value, data) {
        var row = $("<tr />")
        $("#wallets_details").append(row)
        row.append($("<td><a target='_blank' href='https://etherchain.org/account/" + data['address'] + "'>" + data['address'] + "</td>"));
        row.append($("<td>" + data['coin_balance'] + ' ' + data['coin'] + "</td>"));
        row.append($("<td>" + data['fiat_price_str'] + "</td>"));

    })

    $('#settings_investment').val(data['invested'])
    $('#settings_currency').val(data['fiat_currency'])
}
