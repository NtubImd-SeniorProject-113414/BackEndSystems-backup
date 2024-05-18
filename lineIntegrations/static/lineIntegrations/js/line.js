liffToken = '2005031361-7zzGb4xR'
function getLineInfo(){
    liff.init({ liffId: liffToken})
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
