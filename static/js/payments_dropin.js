$(document).ready(function() {
    function braintreeSetup() {
        // Here you tell Braintree to add the drop-in to your division above
        braintree.setup(braintree_client_token, "dropin", {
            container: "braintree-dropin"
            ,onError: function (obj) {
                // Errors will be added to the html code
                $('[type=submit]').prop('disabled', false);
                $('.braintree-notifications').html('<p class="alert alert-danger">' + obj.message + '</p>');
            }
        });
    }
    braintreeSetup();
    $('form').submit(function () {
        $('[type=submit]').prop('disabled', true);
        $('.braintree-notifications').html('');
    });
});