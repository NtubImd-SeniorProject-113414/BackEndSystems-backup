function getLineInfo(){
    liff.init({ liffId: window.register_liff_id})
    .then(async () => {
        if (liff.isLoggedIn()) {
            liff.getProfile().then(profile => {
                $('#lineUid').val(profile.userId);
            });
        } else {
            liff.login();
        }
    })
    .catch((err) => {
        console.log(err);
    })
}
