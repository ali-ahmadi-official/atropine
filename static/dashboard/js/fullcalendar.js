(function () {
  "use strict";

  // Initialize the FullCalendar with updated events
  const curYear = moment().format('YYYY');
  const curMonth = moment().format('MM');
  const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    defaultView: 'month',
    navLinks: true, // can click day/week names to navigate views
    businessHours: true, // display business hours
    editable: true,
    selectable: true,
    selectMirror: true,
    droppable: true, // this allows things to be dropped onto the calendar
      events: [{
          title: 'روز سالانه مدرسه',
          start: moment(curYear + '-' + curMonth + '-02').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-03').format('YYYY-MM-DD'),
          className: "bg-secondary",
          description: 'جشنی برای پایان سال تحصیلی با رویدادها و فعالیت‌های مختلف برای دانش‌آموزان و کارکنان.',
      },
      {
          title: 'نمایشگاه علمی',
          start: moment(curYear + '-' + curMonth + '-17').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-17').format('YYYY-MM-DD'),
          className: "bg-info",
          description: 'دانش‌آموزان پروژه‌های علمی خود را به نمایش می‌گذارند. برای تمامی والدین و دانش‌آموزان باز است.',
      },
      {
          title: 'جلسه والدین و معلمان',
          start: '1404-12-24', // معادل تاریخ شمسی برای 2025-03-15
          end: '1404-12-24',
          className: "bg-primary",
          description: 'یک رویداد مهم که در آن والدین با معلمان ملاقات کرده و پیشرفت فرزندان خود را بررسی می‌کنند.',
      },
      {
          title: 'تعطیلات بهاری',
          start: moment(curYear + '-' + curMonth + '-13').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-13').format('YYYY-MM-DD'),
          className: "bg-warning",
          description: 'دانش‌آموزان برای تعطیلات بهاری استراحت می‌کنند. در این مدت مدرسه تعطیل است.',
      },
      {
          title: 'روز ورزش',
          start: moment(curYear + '-' + curMonth + '-21').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-21').format('YYYY-MM-DD'),
          className: "bg-success",
          description: 'روزی پر از فعالیت‌ها و مسابقات ورزشی. والدین و معلمان نیز دعوت به شرکت دارند.',
      },
      {
          title: 'هفته امتحانات',
          start: '1404-01-21', // معادل شمسی برای 2025-04-10
          end: '1404-01-25',   // معادل شمسی برای 2025-04-14
          className: "bg-success",
          description: 'هفته‌ای که دانش‌آموزان امتحانات پایان ترم خود را برگزار می‌کنند.',
      },
      {
          title: 'جشن‌های ملی',
          start: moment(curYear + '-' + curMonth + '-04T10:00:00').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-06T15:00:00').format('YYYY-MM-DD'),
          className: "bg-info",
          description: 'جشن گرفتن تعطیلات ملی با فعالیت‌های فرهنگی و جشن‌های مختلف.',
      },
      {
          title: 'نمایش مدرسه: رومئو و ژولیت',
          start: moment(curYear + '-' + curMonth + '-23T13:00:00').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-25T18:30:00').format('YYYY-MM-DD'),
          className: "bg-danger",
          description: 'اجرای ویژه توسط باشگاه نمایش مدرسه. همه دانش‌آموزان و خانواده‌ها دعوت به تماشای این نمایش هستند.',
      },
      {
          title: 'روز شغلی',
          start: moment(curYear + '-' + curMonth + '-04').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-04').format('YYYY-MM-DD'),
          className: "bg-success",
          description: 'دانش‌آموزان با مسیرهای شغلی مختلف آشنا می‌شوند و سخنرانانی از حرفه‌های گوناگون حضور خواهند داشت.',
      },
      {
          title: 'روز قدردانی از معلمان',
          start: moment(curYear + '-' + curMonth + '-28').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-28').format('YYYY-MM-DD'),
          className: "bg-teal",
          description: 'روزی برای قدردانی از تلاش و زحمات معلمان مدرسه.',
      },
      {
          title: 'پیک‌نیک مدرسه',
          start: moment(curYear + '-' + curMonth + '-31').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + curMonth + '-31').format('YYYY-MM-DD'),
          className: "bg-pink",
          description: 'پیک‌نیک سرگرم‌کننده در فضای باز برای تمام دانش‌آموزان، معلمان و خانواده‌ها.',
      },
      {
          title: 'شروع تعطیلات تابستانی',
          start: moment(curYear + '-' + '11' + '-11').format('YYYY-MM-DD'),
          end: moment(curYear + '-' + '11' + '-11').format('YYYY-MM-DD'),
          className: "bg-warning",
          description: 'آخرین روز مدرسه قبل از آغاز تعطیلات تابستانی.',
      }
      ],

    eventRender: function (info) {
      // Modify the event's title or description with formatted start and end dates
      const event = info.event;

      // Format the start and end dates as "DD MMMM, YYYY" (e.g., "02 March, 2025")
      const formattedStart = moment(event.start).format('DD MMMM, YYYY');
      const formattedEnd = moment(event.end).format('DD MMMM, YYYY');

      // Add the formatted start and end dates into the event's title or description
      const eventElement = info.el.querySelector('.fc-title');
      if (eventElement) {
        eventElement.innerHTML += `<br><small>From: ${formattedStart} To: ${formattedEnd}</small>`;
      }
    },
    // Handle click on a date in the calendar
    dateClick: function (info) {
      // Trigger the Add Event modal
      const addEventModal = new bootstrap.Modal(document.getElementById('addEvent'));
      addEventModal.show();

      // Clear the date pickers to avoid auto-selection of the clicked date
      document.getElementById('fromDate').value = ''; // Clear the value
      document.getElementById('toDate').value = ''; // Clear the value

      // Optional: Focus on the first input field (event name) for convenience
      document.getElementById('eventName').focus();
    },
    eventClick: function (info) {
      const event = info.event;
      const eventId = event.id;

      // Set data in the Event Details modal (for viewing)
      document.getElementById('modalEventName').textContent = event.title;
      document.getElementById('modalEventDescription').textContent = event.extendedProps.description;

      // Use moment to format the date
      document.getElementById('modalEventStart').textContent = moment(event.start).format("DD MMM, YYYY");
      document.getElementById('modalEventEnd').textContent = event.end ? moment(event.end).format("DD MMM, YYYY") : 'N/A';

      // Show Event Details modal
      const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
      eventModal.show();

      // Add the click event for the Delete button
      document.getElementById('deleteEventButton').onclick = function () {
        // Delete the event from the calendar
        event.remove();
        // Close the modal
        const eventModal = bootstrap.Modal.getInstance(document.getElementById('eventModal'));
        eventModal.hide();
        alert('Event deleted successfully!');
      };
    }
  });

  // Render the calendar
  calendar.render();

  // External Events
  const containerEl = document.getElementById('external-events');
  new FullCalendar.Draggable(containerEl, {
    itemSelector: '.fc-event',
    eventData: function (eventEl) {
      return {
        title: eventEl.innerText.trim(),
        className: eventEl.className + ' overflow-hidden '
      };
    }
  });

  // Handle Add Event Button Click
  document.getElementById('addEventButton').addEventListener('click', function () {
    const eventName = document.getElementById('eventName').value.trim();
    const fromDateStr = document.getElementById('fromDate').value.trim();
    const toDateStr = document.getElementById('toDate').value.trim();
    const eventDescription = document.getElementById('event-description').value.trim();
    const eventType = document.getElementById('eventType').value.trim();

    // Check if all required fields are filled (non-empty)
    if (!eventName || !fromDateStr || !toDateStr || !eventType) {
      alert('Please fill in all fields before adding the event.');
      return; // Exit the function to prevent form submission
    }

    // Convert date strings to YYYY-MM-DD format
    const fromDate = moment(fromDateStr, "DD MMMM, YYYY").format("YYYY-MM-DD");
    const toDate = moment(toDateStr, "DD MMMM, YYYY").format("YYYY-MM-DD");

    const eventClass = eventType;

    // Create a new event
    const newEvent = {
      title: eventName,
      start: fromDate,
      end: toDate,
      description: eventDescription,
      className: eventClass, // Event class for styling
      id: Date.now() // Unique ID for the new event
    };

    calendar.addEvent(newEvent);
    alert('Event added successfully!');

    // Clear the input fields after submitting
    document.getElementById('eventName').value = '';
    document.getElementById('fromDate').value = '';
    document.getElementById('toDate').value = '';
    document.getElementById('event-description').value = '';
    document.getElementById('eventType').value = '';

    // Close the modal
    const addEventModal = bootstrap.Modal.getInstance(document.getElementById('addEvent'));
    addEventModal.hide(); // Correctly hide the modal
  });

  // Date Picker (From Date)
  flatpickr("#fromDate", {
    disableMobile: true,
    minDate: "today",
    defaultDate: null, // Prevent default date selection
    dateFormat: "d F, Y",
    disable: [
      function (date) {
        return date < new Date(); // Disable past dates
      }
    ],
    onOpen: function (selectedDates, dateStr, instance) {
      // Reset the date manually if needed
      instance.clear();
    }
  });

  // Date Picker (To Date)
  flatpickr("#toDate", {
    disableMobile: true,
    minDate: "today",
    defaultDate: null, // Prevent default date selection
    dateFormat: "d F, Y",
    disable: [
      function (date) {
        return date < new Date(); // Disable past dates
      }
    ],
    onOpen: function (selectedDates, dateStr, instance) {
      // Reset the date manually if needed
      instance.clear();
    }
  });


  const myElement1 = document.getElementById('full-calendar-activity');
  new SimpleBar(myElement1, { autoHide: true });

})();
