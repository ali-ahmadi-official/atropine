(function () {
    'use strict';

    /* for basic sweet alert */
    const basicAlertBtn = document.getElementById('basic-alert');
    if (basicAlertBtn) {
        basicAlertBtn.onclick = function () {
            Swal.fire('سلام ، این یک پیام هشدار اساسی است!');
        };
    }
    const alertTextBtn = document.getElementById('alert-text');
    if (alertTextBtn) {
        alertTextBtn.onclick = function () {
            Swal.fire(
                'اینترنت؟',
                'آن چیز هنوز در اطراف است؟',
                'پرسش'
            );
        };
    }
    const alertFooterBtn = document.getElementById('alert-footer');
    if (alertFooterBtn) {
        alertFooterBtn.onclick = function () {
            Swal.fire({
                icon: 'error',
                title: 'اوه ...',
                text: 'مشکلی پیش آمد!',
                footer: '<a href="javascript:void(0);"> چرا این مسئله را دارم؟</a>'
            });
        };
    }
    const longWindowBtn = document.getElementById('long-window');
    if (longWindowBtn) {
        longWindowBtn.onclick = function () {
            Swal.fire({
                title: 'هشدار تصویر قابل پیمایش',
                text: 'این هشدار حاوی یک تصویر بلند برای آزمایش رفتار پیمایش است.',
                imageUrl: 'https://placeholder.pics/svg/300x1500',
                imageHeight: 1500,
                imageAlt: 'یک تصویر بلند'
            });
        };
    }
    
    const alertDescriptionBtn = document.getElementById('alert-description');
    if (alertDescriptionBtn) {
        alertDescriptionBtn.onclick = function () {
            Swal.fire({
                title: '<strong>HTML <u>example</u></strong>',
                icon: 'اطلاعات',
                html: `
                    می توانید استفاده کنید <b>متن فجیع</b>, 
                    <a href="https://sweetalert2.github.io/" target="_blank">links</a>, 
                    و سایر برچسب های HTML.
                `,
                showCloseButton: true,
                showCancelButton: true,
                focusConfirm: false,
                confirmButtonText: '<i class="fe fe-thumbs-up"></i> عالی!',
                confirmButtonAriaLabel: 'انگشت شست ، عالی!',
                cancelButtonText: '<i class="fe fe-thumbs-down"></i>',
                cancelButtonAriaLabel: 'Thumbs down'
            });
        };
    }

    const threeButtonsBtn = document.getElementById('three-buttons');
    if (threeButtonsBtn) {
        threeButtonsBtn.onclick = function () {
            Swal.fire({
                title: 'آیا می خواهید تغییرات را ذخیره کنید؟',
                showDenyButton: true,
                showCancelButton: true,
                confirmButtonText: 'پس انداز کردن',
                denyButtonText: `پس انداز نکنید`,
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire('صرفه جویی!', '', 'موفقیت');
                } else if (result.isDenied) {
                    Swal.fire('تغییرات ذخیره نمی شوند', '', 'اطلاعات');
                }
                // No action for cancel
            });
        };
    }

    const alertDialogBtn = document.getElementById('alert-dialog');
    if (alertDialogBtn) {
        alertDialogBtn.onclick = function () {
            Swal.fire({
                position: 'رده بالا',
                icon: 'موفقیت',
                title: 'کار شما ذخیره شده است',
                showConfirmButton: false,
                timer: 1500
            });
        };
    }

    const alertConfirmBtn = document.getElementById('alert-confirm');
    if (alertConfirmBtn) {
        alertConfirmBtn.onclick = function () {
            Swal.fire({
                title: 'مطمئن هستید؟',
                text: "شما نمی توانید این را برگردانید!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'بله ، آن را حذف کنید!'
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire(
                        'حذف شده!',
                        'پرونده شما حذف شده است.',
                        'موفقیت'
                    );
                }
            });
        };
    }

    const alertParameterBtn = document.getElementById('alert-parameter');
    if (alertParameterBtn) {
        alertParameterBtn.onclick = function () {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success ms-2',
                    cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
            });
    
            swalWithBootstrapButtons.fire({
                title: 'مطمئن هستید؟',
                text: "شما نمی توانید این را برگردانید!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'بله ، آن را حذف کنید!',
                cancelButtonText: 'نه ، لغو!',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    swalWithBootstrapButtons.fire(
                        'حذف شده!',
                        'پرونده شما حذف شده است.',
                        'موفقیت'
                    );
                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    swalWithBootstrapButtons.fire(
                        'لغو شده',
                        'پرونده خیالی شما ایمن است :)',
                        'خطا'
                    );
                }
            });
        };
    }
    
    const alertImageBtn = document.getElementById('alert-image');
    if (alertImageBtn) {
        alertImageBtn.onclick = function () {
            Swal.fire({
                title: 'شیرین!',
                text: 'معین با یک تصویر سفارشی.',
                imageUrl: '../assets/images/media/media-59.jpg',
                imageWidth: 400,
                imageHeight: 200,
                imageAlt: 'تصویر سفارشی'
            });
        };
    }

    const alertCustomBgBtn = document.getElementById('alert-custom-bg');
    if (alertCustomBgBtn) {
        alertCustomBgBtn.onclick = function () {
            Swal.fire({
                title: 'عرض سفارشی ، بالشتک ، رنگ ، پس زمینه.',
                width: 600,
                padding: '3em',
                color: '#716add',
                background: 'url(../assets/images/media/media-19.jpg)',
                backdrop: `
                    rgba(0,0,0,0.3)
                    url(../assets/images/gif%27s/1.gif)
                    left top
                    no-repeat
                `
            });
        };
    }

    const alertAutoCloseBtn = document.getElementById('alert-auto-close');
    if (alertAutoCloseBtn) {
        alertAutoCloseBtn.onclick = function () {
            let timerInterval;

            Swal.fire({
                title: 'هشدار نزدیک خودکار!',
                html: 'من بسته خواهم شد <b></b> هزارم ثانیه.',
                timer: 2000,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                    const b = Swal.getHtmlContainer().querySelector('b');
                    timerInterval = setInterval(() => {
                        b.textContent = Swal.getTimerLeft();
                    }, 100);
                },
                willClose: () => {
                    clearInterval(timerInterval);
                }
            }).then((result) => {
                if (result.dismiss === Swal.DismissReason.timer) {
                    console.log('هشدار به طور خودکار توسط تایمر بسته شد');
                }
            });
        };
    }

    const alertAjaxBtn = document.getElementById('alert-ajax');
    if (alertAjaxBtn) {
        alertAjaxBtn.onclick = function () {
            Swal.fire({
                title: 'نام کاربری GitHub خود را ارسال کنید',
                input: 'متن',
                inputAttributes: {
                    autocapitalize: 'از روی'
                },
                showCancelButton: true,
                confirmButtonText: 'نگاه کردن',
                showLoaderOnConfirm: true,
                preConfirm: (login) => {
                    return fetch(`https://api.github.com/users/${login}`)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`کاربر یافت نشد`);
                            }
                            return response.json();
                        })
                        .catch(error => {
                            Swal.showValidationMessage(`درخواست انجام نشد: ${error}`);
                        });
                },
                allowOutsideClick: () => !Swal.isLoading()
            }).then((result) => {
                if (result.isConfirmed && result.value) {
                    Swal.fire({
                        title: `${result.value.login}'آواتار`,
                        imageUrl: result.value.avatar_url,
                        imageAlt: 'نماد کاربر'
                    });
                }
            });
        };
    }

})();