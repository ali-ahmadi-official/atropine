(function () {
    "use strict"

    // Sample Data
    const productsData = [
        ['SPK001', 'تلویزیون هوشمند 50', '../assets/images/ecommerce/png/19.png', 'تومان699.99', 'در انبار', 'منتشر شده', '120', '8 مهر 1404', 'الکترونیک'],
        ['SPK002', 'کفش های در حال اجرا', '../assets/images/ecommerce/png/18.png', 'تومان89.99', 'خارج از انبار', 'پیش نویس', '0', '8 مهر 1404', 'شیوه'],
        ['SPK003', 'میز ناهار خوری چوبی', '../assets/images/ecommerce/png/17.png', 'تومان399.99', 'در انبار', 'منتشر شده', '45', '8 مهر 1404', 'خانه'],
        ['SPK004', 'گوشواره های بی سیم', '../assets/images/ecommerce/png/16.png', 'تومان129.99', 'در انبار', 'منتشر شده', '250', '8 مهر 1404', 'الکترونیک'],
        ['SPK005', 'ژاکت چرمی', '../assets/images/ecommerce/png/15.png', 'تومان199.99', 'در انبار', 'بایگانی شده', '75', '8 مهر 1404', 'شیوه'],
        ['SPK006', 'صندلی میز کار', '../assets/images/ecommerce/png/14.png', 'تومان149.99', 'خارج از انبار', 'پیش نویس', '0', '8 مهر 1404', 'خانه'],
        ['SPK007', 'بلندگو قابل حمل', '../assets/images/ecommerce/png/13.png', 'تومان79.99', 'در انبار', 'منتشر شده', '300', '8 مهر 1404', 'الکترونیک'],
        ['SPK008', 'لباس تابستانی', '../assets/images/ecommerce/png/12.png', 'تومان59.99', 'در انبار', 'منتشر شده', '150', '8 مهر 1404', 'شیوه'],
        ['SPK009', 'قهوه ساز', '../assets/images/ecommerce/png/11.png', 'تومان59.99', 'در انبار', 'منتشر شده', '60', '8 مهر 1404', 'خانه'],
        ['SPK010', 'کتری برقی', '../assets/images/ecommerce/png/16.png', 'تومان39.99', 'خارج از سهام', 'بایگانی شده', '0', '8 مهر 1404', 'الکترونیک']
    ];

    const grid = new gridjs.Grid({
        columns: [
            {
                name: '#',
                formatter: (_, row) => gridjs.html(
                    `<input class="form-check-input" type="checkbox" id="product-${row.cells[0].data}" value="" aria-label="...">`
                )
            },
            {
                name: 'شناسه محصول',
                formatter: (_, row) => gridjs.html(
                    `<a href="javascript:void(0);">${row.cells[0].data}</a>`  // Correctly map to Product ID (row[0])
                )
            },
            {
                name: 'نام محصول',
                formatter: (_, row) => gridjs.html(
                    `<a href="product-details.html">
                        <div class="d-flex align-items-center gap-3 position-relative">
                            <div class="lh-1">
                                <span class="avatar avatar-lg bg-light">
                                    <img src="${row.cells[2].data}" alt="Product Image">
                                </span>
                            </div>
                            <div>
                                <span class="d-block fw-semibold">${row.cells[1].data}</span>
                                <span class="text-muted fs-13">${row.cells[8].data}</span>
                            </div>
                        </div>
                    </a>`
                )
            },
            'قیمت',
            {
                name: 'وضعیت سهام',
                formatter: (_, row) => gridjs.html(
                    `<span class="badge bg-${row.cells[4].data === 'In Stock' ? 'success' : 'danger'}-transparent">${row.cells[4].data}</span>`
                )
            },
            {
                name: 'مقدار',
                formatter: (_, row) => gridjs.html(
                    `${row.cells[6].data}` // Correctly map to Quantity (row[6])
                )
            },
            {
                name: 'وضعیت',
                formatter: (_, row) => gridjs.html(
                    `<span class="text-${row.cells[5].data === 'Published' ? 'primary' : row.cells[5].data === 'Archived' ? 'success' : 'danger'}">${row.cells[5].data}</span>`
                )
            },
            'تاریخ اضافه شده',
            {
                name: 'اقدامات',
                formatter: (_, row) => gridjs.html(`
                    <div class="dropdown">
                        <a href="javascript:void(0);" class="btn btn-icon btn-sm btn-primary-light border" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fe fe-more-vertical"></i>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="product-details.html"><i class="ri-eye-line me-2"></i>نمایش</a></li>
                            <li><a class="dropdown-item btn-delete" href="javascript:void(0);"><i class="ri-delete-bin-line me-2"></i>حذف کردن</a></li>
                        </ul>
                    </div>
                `)
            }
        ],
        data: productsData,
        pagination: true,
        search: false,
        sort: true
    }).render(document.getElementById('product-table'));

    // Filter functionality: event listeners for input and filter dropdowns
    document.getElementById('search-input').addEventListener('input', (e) => applyFilters());
    document.getElementById('category-filter').addEventListener('change', (e) => applyFilters());
    document.getElementById('status-filter').addEventListener('change', (e) => applyFilters());
    document.getElementById('stock-filter').addEventListener('change', (e) => applyFilters());
    document.getElementById('sort-filter').addEventListener('change', (e) => applyFilters());

    // Function to apply search and filter logic
    function applyFilters() {
        const searchInput = document.getElementById('search-input').value.toLowerCase();
        const categoryFilter = document.getElementById('category-filter').value;
        const statusFilter = document.getElementById('status-filter').value;
        const stockFilter = document.getElementById('stock-filter').value;
        const sortFilter = document.getElementById('sort-filter').value;

        const filteredData = productsData.filter(row => {
            const productName = row[1].toLowerCase();
            const category = row[8].toLowerCase();
            const status = row[5].toLowerCase();
            const stock = row[4].toLowerCase();

            let formattedStock = "";
            if (row[4] === "In Stock") {
                formattedStock = "in-stock";
            } else if (row[4] === "Out of Stock") {
                formattedStock = "out-of-stock";
            }

            const searchCondition = productName.includes(searchInput);
            const categoryCondition = categoryFilter === '' || categoryFilter === 'all' || category === categoryFilter;
            const statusCondition = statusFilter === '' || statusFilter === 'all' || status === statusFilter;
            const stockCondition = stockFilter === '' || stockFilter === 'all' || formattedStock === stockFilter;

            return searchCondition && categoryCondition && statusCondition && stockCondition;
        });

        if (sortFilter) {
            if (sortFilter === 'date') {
                filteredData.sort((a, b) => new Date(b[7]) - new Date(a[7]));
            } else if (sortFilter === 'price') {
                filteredData.sort((a, b) => parseFloat(b[3].replace('$', '')) - parseFloat(a[3].replace('$', '')));
            } else if (sortFilter === 'name') {
                filteredData.sort((a, b) => a[1].localeCompare(b[1]));
            }
        }

        grid.updateConfig({
            data: filteredData
        }).forceRender();

        // Handle the display of the "No matches found" row
        const gridContainer = document.getElementById('product-table');
        const tableBody = gridContainer.querySelector('.gridjs-tbody');

        // Clear previous "No matches found" row
        const notFoundElement = document.querySelector('.gridjs-notfound');
        if (notFoundElement) {
            notFoundElement.style.display = 'none';  // Hide it using JavaScript
        }

        const noMatchesRow = document.getElementById('no-matches-row');
        if (noMatchesRow) {
            noMatchesRow.remove();
        }

        // If no results after filtering, create and append a "No matches found" row
        if (filteredData.length === 0) {
            const tr = document.createElement('tr');
            tr.id = 'no-matches-row';

            // Create a single cell spanning all columns
            const td = document.createElement('td');
            td.colSpan = 9; // Adjust the colspan to match the number of columns
            td.style.textAlign = 'center';
            td.textContent = 'No matching records found';
            td.style.fontWeight = '500';
            td.style.color = 'var(--default-text-color)';
            td.style.padding = '12px';

            tr.appendChild(td);
            tableBody.appendChild(tr);
        }
        
    }

    // Add a listener for delete actions in the table with SweetAlert confirmation
    document.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('btn-delete')) {
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Find the row index of the product to delete
                    const rowIndex = e.target.closest('tr').rowIndex - 1; // Subtract 1 to account for the header row

                    // Remove the product from the productsData array
                    productsData.splice(rowIndex, 1);

                    // Update the grid with the new data
                    grid.updateConfig({
                        data: productsData
                    }).forceRender();

                    Swal.fire(
                        'Deleted!',
                        'Your product has been deleted.',
                        'success'
                    );
                }
            });
        }
    });

})();

    function englishToPersianDigits(str) {
            const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
            return str.replace(/[0-9]/g, d => persianDigits[d]);
        }
    function convertEnglishNumbersToPersian(element = document.body) {
          
            const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    while (walker.nextNode()) {
                const node = walker.currentNode;
    node.nodeValue = englishToPersianDigits(node.nodeValue);
            }
        }
    document.addEventListener("DOMContentLoaded", function () {
        convertEnglishNumbersToPersian();
        });
