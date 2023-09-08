$(document).ready(function() {
    $("#register-form").submit(function(event) {
        event.preventDefault();
        
        var name = $("#name").val();
        var password = $("#password").val();
        
        $.ajax({
            type: "POST",
            url: "/register",
            data: JSON.stringify({ "name": name, "password": password }),
            contentType: "application/json",
            success: function(response) {
                $("#message").html("<p>Kayıt başarıyla tamamlandı!</p>");
            },
            error: function(error) {
                $("#message").html("<p>Kayıt sırasında bir hata oluştu.</p>");
            }
        });
    });
});
