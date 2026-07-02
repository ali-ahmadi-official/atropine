(function () {
    "use strict";

    const tour = new Shepherd.Tour({
        defaultStepOptions: {
            cancelIcon: {
                enabled: true
            },
            classes: 'class-1 class-2',
            scrollTo: { behavior: 'smooth', block: 'center' }
        },
        useModalOverlay: {
            enabled: true,
        }
    });

    tour.addStep({
        id: 'step-1',
        title: "به برنامه تور ما خوش آمدید",
        text: 'تجربه سفر خود را با مقصد ، فعالیت ها و اقامتگاه های دستگیر شده متناسب با ترجیحات شما تنظیم کنید.',
        attachTo: {
            element: '#step-1',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });

    tour.addStep({
        id: 'step-2',
        title: "یک مقصد را انتخاب کنید",
        text: 'مقصدی را انتخاب کنید که با علایق و ترجیحات گروه هماهنگ باشد.',
        attachTo: {
            element: '#step-2',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });

    tour.addStep({
        id: 'Set a Budget',
        title: "حمل و نقل و محل اقامت کتاب",
        text: 'تعیین بودجه ای که حمل و نقل ، اسکان ، وعده های غذایی و فعالیت ها را در بر می گیرد.',
        attachTo: {
            element: '#step-3',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });

    tour.addStep({
        id: 'step-3',
        title: "حمل و نقل و محل اقامت کتاب",
        text: 'حمل و نقل ایمن به مقصد و از مقصد ، و اقامتگاه های مناسب را رزرو کنید.',
        attachTo: {
            element: '#step-4',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });

    tour.addStep({
        id: 'step-5',
        title: "فعالیت های برنامه ریزی",
        text: 'فعالیتهای کلیدی یا جاذبه های مربوط به هر روز تور را تشریح کنید.',
        attachTo: {
            element: '#step-5',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });

    tour.addStep({
        id: 'step-6',
        title: "برقراری ارتباط و تأیید",
        text: 'برنامه سفر را با شرکت کنندگان به اشتراک بگذارید ، رزرو را تأیید کنید و اطمینان حاصل کنید که همه برای تور آماده هستند.',
        attachTo: {
            element: '#step-6',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'بعدی',
                action: tour.next,
            },
        ],
    });
    
    tour.addStep({
        id: 'step-7',
        title: "سفر خود را شروع کنید",
        text: 'برنامه سفر را با شرکت کنندگان به اشتراک بگذارید ، رزرو را تأیید کنید و اطمینان حاصل کنید که همه برای تور آماده هستند.',
        attachTo: {
            element: '#step-7',
            on: 'bottom',
        },
        buttons: [
            {
                text: 'تمام',
                action: tour.next,
            },
        ],
    });

    tour.start();

})();