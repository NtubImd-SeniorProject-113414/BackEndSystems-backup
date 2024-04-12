document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('nav a');
    const nav = document.querySelector('nav');
    const main = document.querySelector('main');
    const accountDropdown = document.getElementById('account-dropdown');
    const account = document.querySelector('.account');

    let isNavOpen = false;

    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const targetURL = this.getAttribute('href');
            if (targetURL === '#') return;

            event.preventDefault();

            const navItems = document.querySelectorAll('nav li');
            navItems.forEach(item => {
                item.classList.remove('active');
            });
            this.parentNode.classList.add('active'); // 正确添加 active 类

            if (isNavOpen) {
                nav.style.animation = 'slideOut 0.5s forwards';
                main.style.animation = 'slideOut 0.5s forwards';
                isNavOpen = false;
            } else {
                nav.style.animation = 'slideIn 0.5s forwards';
                main.style.animation = 'slideIn 0.5s forwards';
                isNavOpen = true;
            }

            setTimeout(() => {
                window.location.href = targetURL;
            }, 500);
        });
    });

    account.addEventListener('click', function (event) {
        event.stopPropagation();
        accountDropdown.classList.toggle('show');
    });

    window.addEventListener('click', function (event) {
        if (!event.target.matches('.account')) {
            if (accountDropdown.classList.contains('show')) {
                accountDropdown.classList.remove('show');
            }
        }
    });

    // 获取当前页面的URL
    const currentURL = window.location.href;

    // 遍历导航链接并检查匹配的链接
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentURL) {
            link.parentNode.classList.add('active');
        }
    });
});
