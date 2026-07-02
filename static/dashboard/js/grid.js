(function () {
    'use script';

    // basic example
    new gridjs.Grid({
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        data: [
            ["۱۴۰۱/۰۸/۰۲ ۱۲:۴۷", "جان", "john123@gmail.com", "#12012", "۱٬۷۹۹٬۰۰۰ تومان", "۱", "۱٬۷۹۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۲۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#12013", "۲٬۴۷۹٬۰۰۰ تومان", "۲", "۴٬۹۵۸٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۲۷ ۱۸:۴۳", "اواین", "eoin1992@gmail.com", "#12014", "۷۶۹٬۰۰۰ تومان", "۱", "۷۶۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۱۹ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#12015", "۱٬۲۹۹٬۰۰۰ تومان", "۳", "۳٬۹۹۷٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۰۵ ۰۹:۵۵", "افشین", "afshin@example.com", "#12016", "۱٬۴۴۹٬۰۰۰ تومان", "۱", "۱٬۴۴۹٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-example1"));
    // basic example

    // with pagination
    new gridjs.Grid({
        pagination: true,
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        data: [
            ["۱۴۰۱/۰۸/۰۲ ۱۲:۴۷", "جان", "john123@gmail.com", "#12012", "۱٬۷۹۹٬۰۰۰ تومان", "۱", "۱٬۷۹۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۲۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#12013", "۲٬۴۷۹٬۰۰۰ تومان", "۲", "۴٬۹۵۸٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۲۷ ۱۸:۴۳", "اواین", "eoin1992@gmail.com", "#12014", "۷۶۹٬۰۰۰ تومان", "۱", "۷۶۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۱۹ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#12015", "۱٬۲۹۹٬۰۰۰ تومان", "۳", "۳٬۹۹۷٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۰۵ ۰۹:۵۵", "افشین", "afshin@example.com", "#12016", "۱٬۴۴۹٬۰۰۰ تومان", "۱", "۱٬۴۴۹٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-pagination"));;
    // with pagination

    // with search
    new gridjs.Grid({
        pagination: true,
        search: true,
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        data: [
            ["۱۴۰۱/۰۸/۰۲ ۱۲:۴۷", "جان", "john123@gmail.com", "#12012", "۱٬۷۹۹٬۰۰۰ تومان", "۱", "۱٬۷۹۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۲۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#12013", "۲٬۴۷۹٬۰۰۰ تومان", "۲", "۴٬۹۵۸٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۲۷ ۱۸:۴۳", "اواین", "eoin1992@gmail.com", "#12014", "۷۶۹٬۰۰۰ تومان", "۱", "۷۶۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۱۹ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#12015", "۱٬۲۹۹٬۰۰۰ تومان", "۳", "۳٬۹۹۷٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۰۵ ۰۹:۵۵", "افشین", "afshin@example.com", "#12016", "۱٬۴۴۹٬۰۰۰ تومان", "۱", "۱٬۴۴۹٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-search"));;
    // with search

    // with sorting
    new gridjs.Grid({
        pagination: true,
        search: true,
        sort: true,
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        data: [
            ["۱۴۰۱/۰۸/۰۲ ۱۲:۴۷", "جان", "john123@gmail.com", "#12012", "۱٬۷۹۹٬۰۰۰ تومان", "۱", "۱٬۷۹۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۲۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#12013", "۲٬۴۷۹٬۰۰۰ تومان", "۲", "۴٬۹۵۸٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۲۷ ۱۸:۴۳", "اواین", "eoin1992@gmail.com", "#12014", "۷۶۹٬۰۰۰ تومان", "۱", "۷۶۹٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۶/۱۹ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#12015", "۱٬۲۹۹٬۰۰۰ تومان", "۳", "۳٬۹۹۷٬۰۰۰ تومان"],
            ["۱۴۰۱/۰۸/۰۵ ۰۹:۵۵", "افشین", "afshin@example.com", "#12016", "۱٬۴۴۹٬۰۰۰ تومان", "۱", "۱٬۴۴۹٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-sorting"));;
    // with sorting

    // loading state
    new gridjs.Grid({
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        pagination: true,
        search: true,
        sort: true,
        data: () => {
            return new Promise(resolve => {
                setTimeout(() =>
                    resolve([
                        ["۱۴۰۱/۰۸/۰۲ ۱۲:۴۷", "جان", "john123@gmail.com", "#۱۲۰۱۲", "۱٬۷۹۹٬۰۰۰ تومان", "۱", "۱٬۷۹۹٬۰۰۰ تومان"],
                        ["۱۴۰۱/۰۶/۲۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#۱۲۰۱۳", "۲٬۴۷۹٬۰۰۰ تومان", "۲", "۴٬۹۵۸٬۰۰۰ تومان"],
                        ["۱۴۰۱/۰۸/۲۷ ۱۸:۴۳", "اوین", "eoin1992@gmail.com", "#۱۲۰۱۴", "۷۶۹٬۰۰۰ تومان", "۱", "۷۶۹٬۰۰۰ تومان"],
                        ["۱۴۰۱/۰۶/۱۹ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#۱۲۰۱۵", "۱٬۲۹۹٬۰۰۰ تومان", "۳", "۳٬۹۹۷٬۰۰۰ تومان"],
                        ["۱۴۰۱/۰۸/۰۵ ۰۹:۵۵", "افشین", "afshin@example.com", "#۱۲۰۱۶", "۱٬۴۴۹٬۰۰۰ تومان", "۱", "۱٬۴۴۹٬۰۰۰ تومان"]
                    ]), 2000);
            });
        }

    }).render(document.getElementById("grid-loading"));
    // loading state

    //wide tables
    new gridjs.Grid({
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شماره سفارش",
            width: "150px",
        }, {
            name: "محصول",
            width: "150px",
        }, {
            name: "دسته‌بندی",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "مجموع",
            width: "100px",
        }],
        style: {
            table: {
                'white-space': 'nowrap'
            }
        },
        resizable: true,
        sort: true,
        pagination: true,
        data: [
            ["۰۲ آبان ۱۴۰۱ ۱۲:۴۷", "جان", "john123@gmail.com", "#۱۲۰۱۲", "ساعت هوشمند", "الکترونیک", "۵۵٬۰۰۰٬۰۰۰ تومان", "۱", "۵۵٬۰۰۰٬۰۰۰ تومان"],
            ["۲۱ شهریور ۱۴۰۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#۱۲۰۱۳", "شلوار جین آبی", "لباس", "۷۶٬۰۰۰٬۰۰۰ تومان", "۲", "۱۵۲٬۰۰۰٬۰۰۰ تومان"],
            ["۲۷ آبان ۱۴۰۱ ۱۸:۴۳", "اوین", "eoin1992@gmail.com", "#۱۲۰۱۴", "گوشی جی", "موبایل", "۲۳٬۵۰۰٬۰۰۰ تومان", "۱", "۲۳٬۵۰۰٬۰۰۰ تومان"],
            ["۱۹ شهریور ۱۴۰۱ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#۱۲۰۱۵", "هدفون", "الکترونیک", "۳۹٬۸۰۰٬۰۰۰ تومان", "۳", "۱۱۹٬۴۰۰٬۰۰۰ تومان"],
            ["۵ آبان ۱۴۰۱ ۰۹:۵۵", "افشین", "afshin@example.com", "#۱۲۰۱۶", "صندلی", "مبلمان", "۴۴٬۵۰۰٬۰۰۰ تومان", "۱", "۴۴٬۵۰۰٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-wide"));
    //wide tables

    // fixed header
    new gridjs.Grid({
        pagination: true,
        search: true,
        sort: true,
        fixedHeader: true,
        height: '350px',
        columns: [{
            name: "تاریخ",
            width: "150px",
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "مجموع",
            width: "100px",
        }],
        data: [
            ["۰۲ آبان ۱۴۰۱ ۱۲:۴۷", "جان", "john123@gmail.com", "#۱۲۱۰۲", "۶۷٬۸۰۰٬۰۰۰ تومان", "۱", "۶۷٬۸۰۰٬۰۰۰ تومان"],
            ["۲۱ شهریور ۱۴۰۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#۱۲۱۰۳", "۹۳٬۲۲۰٬۰۰۰ تومان", "۲", "۱۸۶٬۴۴۰٬۰۰۰ تومان"],
            ["۲۷ آبان ۱۴۰۱ ۱۸:۴۳", "ئوین", "eoin1992@gmail.com", "#۱۲۱۰۴", "۲۸٬۹۲۰٬۰۰۰ تومان", "۱", "۲۸٬۹۲۰٬۰۰۰ تومان"],
            ["۱۸ شهریور ۱۴۰۱ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#۱۲۱۰۵", "۴۸٬۹۷۰٬۰۰۰ تومان", "۳", "۱۴۶٬۹۱۰٬۰۰۰ تومان"],
            ["۵ آبان ۱۴۰۱ ۰۹:۵۵", "افشین", "afshin@example.com", "#۱۲۱۰۶", "۵۴٬۶۵۰٬۰۰۰ تومان", "۱", "۵۴٬۶۵۰٬۰۰۰ تومان"],
            ["۰۲ آبان ۱۴۰۱ ۱۲:۴۷", "جان", "john123@gmail.com", "#۱۲۱۰۲", "۶۷٬۸۰۰٬۰۰۰ تومان", "۱", "۶۷٬۸۰۰٬۰۰۰ تومان"],
            ["۲۱ شهریور ۱۴۰۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#۱۲۱۰۳", "۹۳٬۲۲۰٬۰۰۰ تومان", "۲", "۱۸۶٬۴۴۰٬۰۰۰ تومان"],
            ["۲۷ آبان ۱۴۰۱ ۱۸:۴۳", "ئوین", "eoin1992@gmail.com", "#۱۲۱۰۴", "۲۸٬۹۲۰٬۰۰۰ تومان", "۱", "۲۸٬۹۲۰٬۰۰۰ تومان"],
            ["۱۸ شهریور ۱۴۰۱ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#۱۲۱۰۵", "۴۸٬۹۷۰٬۰۰۰ تومان", "۳", "۱۴۶٬۹۱۰٬۰۰۰ تومان"],
            ["۵ آبان ۱۴۰۱ ۰۹:۵۵", "افشین", "afshin@example.com", "#۱۲۱۰۶", "۵۴٬۶۵۰٬۰۰۰ تومان", "۱", "۵۴٬۶۵۰٬۰۰۰ تومان"],
            ["۰۲ آبان ۱۴۰۱ ۱۲:۴۷", "جان", "john123@gmail.com", "#۱۲۱۰۲", "۶۷٬۸۰۰٬۰۰۰ تومان", "۱", "۶۷٬۸۰۰٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-header-fixed"));
    // fixed header

    // hidden columns
    new gridjs.Grid({
        columns: [{
            name: "تاریخ",
            hidden: true,
        }, {
            name: "نام",
            width: "150px",
        }, {
            name: "ایمیل",
            width: "200px",
        }, {
            name: "شناسه",
            width: "150px",
        }, {
            name: "قیمت",
            width: "100px",
        }, {
            name: "تعداد",
            width: "100px",
        }, {
            name: "جمع کل",
            width: "100px",
        }],
        sort: true,
        search: true,
        pagination: true,
        data: [
            ["۰۲/۰۸/۱۴۰۱ ۱۲:۴۷", "جان", "john123@gmail.com", "#12012", "۷۵٬۰۰۰٬۰۰۰ تومان", "۱", "۷۵٬۰۰۰٬۰۰۰ تومان"],
            ["۲۱/۰۶/۱۴۰۱ ۰۴:۲۴", "مارک", "markzenner23@gmail.com", "#12013", "۱۰۳٬۰۰۰٬۰۰۰ تومان", "۲", "۲۰۶٬۰۰۰٬۰۰۰ تومان"],
            ["۲۷/۰۸/۱۴۰۱ ۱۸:۴۳", "اوئین", "eoin1992@gmail.com", "#12014", "۳۲٬۰۰۰٬۰۰۰ تومان", "۱", "۳۲٬۰۰۰٬۰۰۰ تومان"],
            ["۱۹/۰۶/۱۴۰۱ ۱۰:۳۵", "سارا", "sarahcdd129@gmail.com", "#12015", "۵۴٬۰۰۰٬۰۰۰ تومان", "۳", "۱۶۲٬۰۰۰٬۰۰۰ تومان"],
            ["۵/۰۸/۱۴۰۱ ۰۹:۵۵", "افشین", "afshin@example.com", "#12016", "۶۰٬۰۰۰٬۰۰۰ تومان", "۱", "۶۰٬۰۰۰٬۰۰۰ تومان"]
        ],

    }).render(document.getElementById("grid-hidden-column"));;
    // hidden columns

})();