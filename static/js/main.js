document.addEventListener("DOMContentLoaded", function () {

    let selectedFilter = "";
    const assumptionSelect = document.getElementById('assumptions-select');
    const mobileToggleElements = document.querySelectorAll('.jb-aside-mobile-toggle');
    const toggleDropdownElement = document.getElementById('toggleDropdown');
    const menuListElements = document.querySelectorAll('.menu-list li');
    const manualDiv = document.getElementById('manual-div')
    const formulaDiv = document.getElementById('formula-div')
    const modalElements = document.querySelectorAll('.jb-modal');
    const modalCloseElements = document.querySelectorAll('.jb-modal-close');
    const checkbElements = document.querySelectorAll('.checkb');
    const entryType = document.getElementById('entry_type');
    const search = document.getElementById('account-input-search');
    const asideToggle = document.querySelector('.jb-aside-toggle')
    const criteria = document.getElementById('search-criteria');
    const tableBody = document.getElementById('table-body');
    const evenlyCB = document.getElementById('evenly')
    const monthsCB = document.getElementById('months')
    const quarterCB = document.getElementById('quarter')

    const quarterDiv = document.getElementById('quarter-div')
    const navigateToBudget = document.getElementById('navigateToBudget')
    const toggleCards = document.getElementById('toggleCards')
    const checkbox = document.getElementById('non-zero')
    const deptList = document.querySelectorAll('a.dropdown-item.dept-list')
    const parentAccordion = document.querySelectorAll(".card-header-icon.accordion-button")
    const childAccordion = document.querySelectorAll(".child-accordion-button")
    const notficDismiss = document.querySelectorAll(".jb-notification-dismiss")
    const chngeNotification = document.getElementById("change-notification")
    const monthsDiv = document.getElementById('months-div')
    const submitBtn = document.getElementById('submitButton')
    const formDiv = document.getElementById('add-line')
    const button2Element = document.querySelector("[id='changeButton']");
    const buttonElement = document.querySelector("[id='settingsSubmitButton']");
    const rate = document.getElementById('rate')
    const factor = document.getElementById('factor')
    let quarter = []
    let mths = []
    if (buttonElement) {
        buttonElement.addEventListener("click", function (ev) {
            ev.preventDefault()
            const objId = buttonElement.getAttribute('data-id');
            localStorage.setItem("showUploadNotification", "true");
            let comment = document.getElementById('comments').value
            fetch(`/settings?complete=${1}&budget_id=${objId}&comment=${comment}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(result => {
                    var match = objId.match(/\d+/);

                    if (match) {
                        var currentNumber = parseInt(match[0]);
                        var newNumber = currentNumber + 1;

                        // Construct the updated objId with the incremented number
                        var updatedObjId = objId.replace(/\d+/, newNumber);

                        // Update the window location with the new objId
                        window.location.reload();
                    }
                })

        });
    }
    if (button2Element) {
        button2Element.addEventListener("click", function (ev) {
            ev.preventDefault()
            const objId = button2Element.getAttribute('data-id');
            let comment = document.getElementById('comments').value
            localStorage.setItem("showChangeNotification", "true");
            fetch(`/settings?incomplete=${1}&budget_id=${objId}&comment=${comment}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(result => {
                    window.location.reload()
                })

        });


    }
    document.querySelectorAll('.jb-navbar-menu-toggle').forEach(el => {
        el.addEventListener('click', e => {
            const dropdownIcon = e.currentTarget.querySelector('.icon .mdi');
            const targetId = e.currentTarget.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);

            targetElement.classList.toggle('is-active');
            dropdownIcon.classList.toggle('mdi-dots-vertical');
            dropdownIcon.classList.toggle('mdi-close');
        });
    });


    if (navigateToBudget) {
        navigateToBudget.addEventListener('change', (ev) => {
            window.location.href = "/home/" + ev.target.value;
        })
    }
    if (toggleCards) {
        toggleCards.addEventListener('click', () => {
            document.getElementById('dashboard-cards').classList.toggle('is-hidden');
        })
    }

    if (checkbox) {
        checkbox.addEventListener('change', function (event) {
            const rows = document.querySelectorAll('.budget-table-body tr');
            if (event.target.checked) {
                // Show non-zero rows
                rows.forEach(row => {
                    if (row.dataset.total !== "0.00") {
                        row.style.display = "table-row";
                    } else {
                        row.style.display = "none";
                    }
                });
            } else {
                // Show all rows
                rows.forEach(row => {
                    row.style.display = "table-row";
                });
            }
        })
    }
    if (deptList.length > 0) {

        deptList.forEach(dept => {
            dept.addEventListener('click', (ev) => {
                ev.preventDefault();
                var dept_id = dept.getAttribute('data-deptid');
                window.location.href = '/update/expenses/' + dept_id;
            });
        })
    }
     if (parentAccordion.length > 0) {
        parentAccordion.forEach(function(button) {
            button.addEventListener("click", function () {
                const parentHeader = this.closest("header");
                const parentAccordionContent = parentHeader.nextElementSibling;

                if (parentAccordionContent.classList.contains("parent-accordion-content")) {
                    // Toggle visibility of the accordion content
                    parentAccordionContent.classList.toggle("is-hidden");

                    // Update the icon
                    const icon = this.querySelector("i");
                    if (parentAccordionContent.classList.contains("is-hidden")) {
                        icon.classList.remove("mdi-minus-thick");
                        icon.classList.add("mdi-plus-thick");
                    } else {
                        icon.classList.remove("mdi-plus-thick");
                        icon.classList.add("mdi-minus-thick");
                    }

                    let deptId = parentAccordionContent.dataset.department;
                    console.log(deptId);
                    addEventListenerToAnchorTag(deptId); // Ensure this function is defined elsewhere
                }
                const subAccordionButtons = parentAccordionContent.querySelectorAll('.sub-group-container .accordion-button');
                if (subAccordionButtons) {
                    subAccordionButtons.forEach(function (subButton) {
                        subButton.addEventListener("click", function () {
                            const subHeader = this.closest("header");
                            const subAccordionContent = subHeader.nextElementSibling;

                            if (subAccordionContent.classList.contains("sub-accordion-content")) {
                                // Toggle visibility of the sub-group accordion content
                                subAccordionContent.classList.toggle("is-hidden");

                                // Update the icon for the sub-group
                                const subIcon = this.querySelector("i");
                                if (subAccordionContent.classList.contains("is-hidden")) {
                                    subIcon.classList.remove("mdi-minus-thick");
                                    subIcon.classList.add("mdi-plus-thick");
                                } else {
                                    subIcon.classList.remove("mdi-plus-thick");
                                    subIcon.classList.add("mdi-minus-thick");
                                }
                            }
                        });
                    });
                }
            })
        })

    }



    if (localStorage.getItem("showUploadNotification")) {
        const upNotification = document.getElementById("upload-notification")
        if (upNotification) {
            upNotification.classList.remove('is-hidden');
            notficDismiss.forEach(function (notf) {
                notf.addEventListener("click", function () {
                    localStorage.removeItem("showUploadNotification");
                    upNotification.classList.add('is-hidden');
                });
            })
        }
    } else if (localStorage.getItem("showChangeNotification")) {
        if (chngeNotification && notficDismiss) {
            chngeNotification.classList.remove('is-hidden');
            notficDismiss.forEach(function (notf) {
                notf.addEventListener("click", function () {
                    localStorage.removeItem("showChangeNotification");
                    chngeNotification.classList.add('is-hidden');
                });
            })
        }
    } else {
        if (notficDismiss) {
            notficDismiss.forEach(function (notf) {
                notf.addEventListener("click", function () {
                    let notifications = document.querySelectorAll('.notification')
                    localStorage.removeItem("showUploadNotification");
                    localStorage.removeItem("showChangeNotification");
                    notifications.forEach(function (notification) {
                        notification.classList.add('is-hidden');
                    });

                });
            })
        }
    }

 function getCSRFToken() {
        let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
        if (csrfToken == null) {
            csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        }
        return csrfToken;
    }
//setup chat scoket
    const notifyScoket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/notify/'
    );

// on socket open
    if (notifyScoket.readyState === WebSocket.OPEN) {
        // WebSocket is already open, no need to open it again
    } else {
        // WebSocket is not open, open it
        notifyScoket.onopen = function (e) {
            console.log('Socket successfully connected.');
        };

        notifyScoket.onclose = function (e) {
            console.log('Socket closed unexpectedly');
        }
    }
// on receiving message on group
    notifyScoket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        setMessage(message);


    };
    function setMessage(message) {
  // Generate a unique notification ID
  const notificationId = generateNotificationId();

  // Create a new notification object with the message and ID
  const notification = {
    id: notificationId,
    message: message
  };

  // Save the notification object in local storage
  const notifications = JSON.parse(localStorage.getItem('notifications')) || [];
  notifications.push(notification);
  localStorage.setItem('notifications', JSON.stringify(notifications));

  // Create the new notification element
  const newAnchor = document.createElement('a');
  newAnchor.className = 'navbar-item is-clipped is-size-7';
  newAnchor.textContent = message;
  newAnchor.style.wordBreak = 'break-word';
  newAnchor.id = notificationId;

  // Append the new notification element to the notification container
  const divElement = document.getElementById('notify');
  divElement.appendChild(newAnchor);
    markAsRead(notification.id)
  // Update the notification count
  const count = document.getElementById('bellCount').getAttribute('data-count');
  document.getElementById('bellCount').setAttribute('data-count', parseInt(count) + 1);
}

function generateNotificationId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}


function markAsRead(notificationId) {
  var anchorElement = document.getElementById(notificationId);
if (anchorElement) {
    anchorElement.addEventListener('click', () => {
        // Remove the notification from local storage
        const notifications = JSON.parse(localStorage.getItem('notifications')) || [];
        const updatedNotifications = notifications.filter(notification => notification.id !== notificationId);
        localStorage.setItem('notifications', JSON.stringify(updatedNotifications));

        // Hide the notification element
        anchorElement.classList.add('is-hidden');
        const count = document.getElementById('bellCount').getAttribute('data-count');
        document.getElementById('bellCount').setAttribute('data-count', parseInt(count) - 1);

        // Redirect to the desired page (e.g., "/settings")
        //window.location.href = "/settings";
    });
}
}

function loadNotifications() {
  const notifications = JSON.parse(localStorage.getItem('notifications')) || [];

  notifications.forEach(notification => {
    const newAnchor = document.createElement('a');
    newAnchor.className = 'navbar-item is-clipped is-size-7';
    newAnchor.textContent = notification.message;
    newAnchor.style.wordBreak = 'break-word';
    newAnchor.id = notification.id;

    const divElement = document.getElementById('notify');
    if (divElement){
        divElement.appendChild(newAnchor);

    }
    const bell = document.getElementById('bellCount')
      if (bell){
        const count = bell.getAttribute('data-count');
        bell.setAttribute('data-count', parseInt(count) + 1);
      }

    // Add event listener to mark notification as read
    newAnchor.addEventListener('click', () => {
      markAsRead(notification.id);
    });
  });
}
loadNotifications()

    if (asideToggle) {
        asideToggle.addEventListener('click', function () {
            // Check if the aside is being hidden
            if (document.querySelector('.aside').classList.contains('is-narrow')) {
                // Adjust the width of the app div when the aside is hidden
                document.getElementById('app').style.width = '100%'; // Adjust the width as needed
            } else {
                // Reset the width of the app div when the aside is shown
                document.getElementById('app').style.width = 'calc(100% - 250px)'; // Adjust the width as needed
            }
        });
    }
// Toggle mobile aside


    if (mobileToggleElements.length > 0) {
        mobileToggleElements.forEach(el => {
            el.addEventListener('click', e => {
                const dropdownIcon = e.currentTarget.querySelector('.icon .mdi');
                document.documentElement.classList.toggle('has-aside-mobile-expanded');
                dropdownIcon.classList.toggle('mdi-forwardburger');
                dropdownIcon.classList.toggle('mdi-backburger');
            });
        });
    }

// Toggle menu list items


    document.querySelectorAll('.menu-list li').forEach(el => {
        el.addEventListener('click', e => {
            e.currentTarget.classList.toggle('is-active');
            const dropdownIcon = e.currentTarget.querySelector('.dropdown-icon .icon i');
            dropdownIcon.classList.toggle('mdi-plus');
            dropdownIcon.classList.toggle('mdi-minus');
            e.stopPropagation()


        });
    });

// Open modal
    if (modalElements.length > 0) {
        modalElements.forEach(el => {
            el.addEventListener('click', e => {
                const modalTarget = e.currentTarget.getAttribute('data-target');
                document.getElementById(modalTarget).classList.add('is-active');
                document.documentElement.classList.add('is-clipped');
            });
        });
    }

// Close modal
    if (modalCloseElements.length > 0) {
        modalCloseElements.forEach(el => {
            el.addEventListener('click', e => {
                e.currentTarget.closest('.modal').classList.remove('is-active');
                document.documentElement.classList.remove('is-clipped');
            });
        });
    }
    /* Notification dismiss */


    if (search && criteria && tableBody) {
        // Add event listener to search input
        criteria.addEventListener('change', (ev) => {
            search.removeAttribute('disabled');
            selectedFilter = ev.target.value;
        });

        search.addEventListener('input', (ev) => {
            const val = ev.target.value.trim();

            if (val === "") {
                tableBody.innerHTML = "";
                return;
            }
            // Fetch data based on search criteria
            fetch(`/account/search?filter=${selectedFilter}&value=${val}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(result => {
                    const data = result.data;
                    tableBody.innerHTML = "";
                    data.forEach(item => {
                        // Create table rows based on fetched data
                        const row = document.createElement('tr');
                        const anchorID = document.createElement('a');
                        anchorID.href = `/update/${item.id}`;
                        anchorID.textContent = item.account_id;
                        anchorID.classList.add('has-text-black');

                        const anchorName = document.createElement('a');
                        anchorName.href = `/update/${item.id}`;
                        anchorName.textContent = item.account__acctdesc;
                        anchorName.classList.add('has-text-black');

                        const cell1 = document.createElement('td');
                        const cell2 = document.createElement('td');
                        cell1.appendChild(anchorID);
                        cell2.appendChild(anchorName);

                        row.appendChild(cell1);
                        row.appendChild(cell2);

                        tableBody.appendChild(row);
                    });
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        });
    }

// Check for the existence of other elements and add event listeners accordingly
// Add event listeners to checkboxes
    if (checkbElements.length > 0) {
        checkbElements.forEach(cb => {
            cb.addEventListener('click', handleCheck);
        });
    }

// Function to handle checkbox clicks to specify amount distribution
    function handleCheck() {
        if (evenlyCB.checked) {
            monthsCB.checked = false
            quarterCB.checked = false
            monthsDiv.classList.add('is-hidden')
            quarterDiv.classList.add('is-hidden')

        } else if (monthsCB.checked) {
            evenlyCB.checked = false
            quarterCB.checked = false
            monthsDiv.classList.remove('is-hidden')
            quarterDiv.classList.add('is-hidden')
            document.querySelectorAll('.variableCheckbox').forEach(function (checkbox) {
                checkbox.addEventListener('change', function () {
                    mths = [];
                    let checkedBoxes = document.querySelectorAll('.variableCheckbox:checked');
                    checkedBoxes.forEach(function (checkbox) {
                        mths.push(checkbox.value);
                    });

                });
            });
        } else if (quarterCB.checked) {
            monthsCB.checked = false
            evenlyCB.checked = false
            quarterDiv.classList.remove('is-hidden')
            monthsDiv.classList.add('is-hidden')
            document.querySelectorAll('.quaterlyCheckbox').forEach(function (checkbox) {
                checkbox.addEventListener('change', function () {
                    quarter = [];
                    let checkedBoxes = document.querySelectorAll('.quaterlyCheckbox:checked');
                    checkedBoxes.forEach(function (checkbox) {
                        quarter.push(checkbox.value);
                    });
                });
            });

        } else {
            monthsDiv.classList.add('is-hidden')
            quarterDiv.classList.add('is-hidden')
        }
    }

// Add event listener to entryType select element
    if (entryType) {
        entryType.addEventListener('change', () => {
            const currentUrl = window.location.href;
            submitBtn.disabled = false
            document.getElementById('add-line').classList.remove('is-hidden')
            if (entryType.value === 'formula') {
                assumptionSelect.disabled = false
                document.getElementById('form-settings-modal').classList.add('is-active');
                manualDiv.classList.add('is-hidden')
                formulaDiv.classList.remove('is-hidden');
                if (currentUrl.includes('update')) {
                $(".manual-input").each(function (index, el) {
                    $(el).val('0');
                });
                }
            } else if (entryType.value === 'manual') {
                formulaDiv.classList.add('is-hidden');
                manualDiv.classList.remove('is-hidden')
                document.getElementById('form-settings-modal').classList.remove('is-active');
                assumptionSelect.disabled = true;
                if (currentUrl.includes('update')) {
                $(".formula-input").each(function (index, el) {
                    $(el).val('0');
                });
                }
            } else {
                submitBtn.disabled = true
            }
        });
    }
    if (assumptionSelect) {
        assumptionSelect.addEventListener('change', () => {
           const selectedIndex = assumptionSelect.selectedIndex;
            if (selectedIndex !== -1) {
                const selectedOption = assumptionSelect.options[selectedIndex];
                const selectedRate = selectedOption.getAttribute('data-value');
                console.log(selectedRate)
                if (selectedRate) {
                    rate.value = selectedRate;
                    rate.readOnly = true;
                } else {
                    // Handle the case where data-rate is not set
                    console.error('data-rate attribute is not set for the selected option.');
                }
        }
        })
    }
// Add event listeners to buttons with class 'is-info'
    if (submitBtn) {
         let objctId = null;
        submitBtn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default form submission
            if (!window.location.href.includes('update')) {
               let rawObj = submitBtn.dataset.objectidentification.replace(',','')
                objctId = parseInt(rawObj)
            }

            let isValid = true;
            $('.manual-input, .formula-input').each(function () {
                if (!handleError($(this))) {
                    isValid = false;
                }
            });
            if (isValid) {
                const selectedOption = entryType.value;
                const formData = {};
                $(".overall").each((index, el) => {
                    formData[$(el).attr('name')] = $(el).val() || 1;
                })
                const selectedCurrencyOption = document.getElementById('currency').selectedOptions[0];

                if (selectedOption === 'formula') {
                    $(".formula-input").each((index, el) => {
                        formData[$(el).attr('name')] = parseFloat($(el).val()) || 0;

                    })
                    const assumption = (document.getElementById('assumptions-select')?.selectedOptions[0]?.textContent) || 'None';

                    const rate = selectedCurrencyOption.dataset.rate;
                    let total
                    const nonZeroVariables = [formData['rate'], formData['usage'], formData['factor'], formData['staff']].filter(value => value !== 0);
                    if (nonZeroVariables.length > 0) {
                        total = nonZeroVariables.reduce((accumulator, currentValue) => accumulator * currentValue);
                        total = total * rate
                        formData['total'] = total;
                    }

                    if (evenlyCB.checked) {
                        let dividend = total / 12
                        for (let i = 1; i <= 12; i++) {
                            formData['netperd' + i] = dividend
                        }
                    } else if (monthsCB.checked) {
                        let dividend = total / mths.length;

                        const monthToNumber = {
                            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                        };

                        // Set values for months in mths array
                        for (let i = 0; i < mths.length; i++) {
                            formData['netperd' + monthToNumber[mths[i].toLowerCase()]] = dividend;
                        }

                        // Set values to 0 for months not in mths array
                        const allMonths = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
                        allMonths.forEach(month => {
                            if (!mths.includes(month)) {
                                formData['netperd' + monthToNumber[month]] = 0;
                            }
                        });

                    } else if (quarterCB.checked) {
                        let dividend = total / quarter.length;

                        const quarterToNumber = {
                            'q1': 3, 'q2': 6, 'q3': 9, 'q4': 12,
                        };

                        // Set values for months in mths array
                        for (let i = 0; i < quarter.length; i++) {
                            formData['netperd' + quarterToNumber[quarter[i]]] = dividend;
                        }

                        // Corrected loop to set values for all months
                        for (let i = 1; i <= 12; i++) {
                            if (!formData.hasOwnProperty('netperd' + i)) {
                                formData['netperd' + i] = 0;
                            }
                        }
                    }
                    formData['exchange_rate'] = rate
                    formData['entryType'] = 'function'
                    formData['assumption'] = assumption
                    console.log(formData)
                    $.ajax({
                        url: ``,
                        type: 'POST',
                        data: JSON.stringify(formData),
                        headers: {'X-CSRFToken': getCSRFToken()}, // Include CSRF token
                        success: function (resp) {
                            if (window.location.href.includes('update')) {
                                window.location.href = ``
                            } else {
                                window.location.href = `/update/${objctId}`
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log("Error status: " + status);
                            console.log("Error message: " + error);
                            console.log(xhr.responseText); // Log the full response for detailed error information
                            // Handle the error or display a specific message to the user
                        }
                    });
                } else if (selectedOption === 'manual') {


                    const rate = selectedCurrencyOption.dataset.rate;

                    $(".manual-input").each((index, el) => {
                        formData[$(el).attr('name')] = parseFloat($(el).val()) * rate || 0;
                    });

                    formData['exchange_rate'] = rate
                    formData['entryType'] = 'manual'
                    let total = 0
                    for (let i = 1; i <= 12; i++) {
                        if (formData['netperd' + i] !== '') {
                            total += parseFloat(formData['netperd' + i])
                        }
                    }
                    formData['total'] = total
                    console.log(formData)
                    $.ajax({
                        url: ``,
                        type: 'POST',

                        data: JSON.stringify(formData),
                        headers: {'X-CSRFToken': getCSRFToken()}, // Include CSRF token
                        success: function (resp) {

                            if (window.location.href.includes('update')) {
                                window.location.href = ``
                            } else {
                                window.location.href = `/update/${objctId}`
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log("Error status: " + status);
                            console.log("Error message: " + error);
                            console.log(xhr.responseText); // Log the full response for detailed error information
                            // Handle the error or display a specific message to the user
                        }
                    });
                }
            }
        });

    }

// Add event listener to toggleDropdown element
    document.querySelectorAll('.dropdown').forEach(function(dropdown) {
    const trigger = dropdown.querySelector('.dropdown-trigger button');

    trigger.addEventListener('click', function(event) {
        // Close other active dropdowns
        document.querySelectorAll('.dropdown.is-active').forEach(function(otherDropdown) {
            if (otherDropdown !== dropdown) {
                otherDropdown.classList.remove('is-active');
            }
        });

        // Toggle the 'is-active' class on the clicked dropdown
        dropdown.classList.toggle('is-active');
    });
});

// Close the dropdown if clicking outside of it
document.addEventListener('click', function(event) {
    const target = event.target;
    document.querySelectorAll('.dropdown.is-active').forEach(function(dropdown) {
        if (!dropdown.contains(target)) {
            dropdown.classList.remove('is-active');
        }
    });
});


    const handleError = (input) => {
        let inputValue = input.val().trim();
        let decimalPattern = /^-?(?!0\d)\d*(\.\d{1,2})?$/;
        let errorMessage = '<p class="help is-danger">Please enter a valid number</p>';

        if (!decimalPattern.test(inputValue)) {
            input.addClass('is-danger');
            input.next('.help').remove();
            input.after(errorMessage);
            return false; // Return false for invalid input
        } else {
            input.removeClass('is-danger');
            input.next('.help').remove();
            return true; // Return true for valid input
        }
    };

    $('.manual-input').blur(function () {
        handleError($(this));
    });

    $('.formula-input').blur(function () {
        handleError($(this));
    });

    function preprocessData(data) {
        let decimalPattern = /^-?(?!0\d)\d*(\.\d{1,2})?$/
        // Check each value for a percentage sign and convert it to decimal if found
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                // Check if the key is 'rate'
                if (key === 'rate' && typeof data[key] === 'string') {
                    // Remove comma separators from the value
                    data[key] = data[key].replace(/,/g, '').replace(/-/g, '');

                }
                // Check if the value contains a percentage sign
                if (typeof data[key] === 'string' && data[key].indexOf('%') !== -1) {
                    // Remove the percentage sign and convert to decimal
                    data[key] = parseFloat(data[key].replace('%', '')) / 100;

                }
            }
        }
        return data;
    }

    $(document).on("click", ".editBtn", function () {
            var action = $(this).data("action");
            var target = $(this).data("target");
            if (action === "edit") {
                var row = $(this).closest("tr");
                var cells = row.find("td").not(":last-child");
                cells.each(function (index) {
                    var currentValue = $(this).text();
                    if (index === 1) {
                        $(this).html('<input type="text" class="input " onblur="handleError($(this))" value="' + currentValue + '">');
                    } else {
                        $(this).html('<input type="text" class="input" value="' + currentValue + '">');
                    }


                })

                $(this).data("action", "save").find("i").removeClass("mdi-file-edit").addClass("mdi-plus");
            } else if (action === "save" && target === "assumptions") {
                var row = $(this).closest("tr");
                var cells = row.find("td").not(":last-child");
                var newData = {};
                newData['target'] = "assumptions"
                cells.each(function (index) {
                    if (index === 0) {

                        newData['factor'] = $(this).find("input").val();
                        $(this).text($(this).find("input").val());
                    } else if (index === 1) {

                        newData['rate'] = $(this).find("input").val();
                        $(this).text($(this).find("input").val());
                    }
                });
                // Assuming you have a function to send data to backend
                sendDataToBackend(newData, function () {
                    $(this).data("action", "edit").find("i").removeClass("mdi-plus").addClass("mdi-file-edit");
                }.bind(this));
            } else if (action === "save" && target === "currency") {
                var row = $(this).closest("tr");
                var cells = row.find("td").not(":last-child");
                var newData = {};
                newData['target'] = "currency"
                cells.each(function (index) {
                    if (index === 0) {

                        newData['currency'] = $(this).find("input").val();
                        $(this).text($(this).find("input").val());
                    } else if (index === 1) {

                        newData['rate'] = $(this).find("input").val();
                        $(this).text($(this).find("input").val());
                    }
                });
                // Assuming you have a function to send data to backend
                sendDataToBackend(newData, function () {
                    $(this).data("action", "edit").find("i").removeClass("mdi-plus").addClass("mdi-file-edit");
                }.bind(this));
            }
        }
    )
    ;

    function sendDataToBackend(data, callback) {
        // Perform AJAX request to send data to the backend
        var processedData = preprocessData(data);
        $.ajax({
            url: "/update/assumptions/",
            method: "POST",
            data: JSON.stringify(processedData),
            headers: {'X-CSRFToken': getCSRFToken()},
            success: function (response) {
                // Call the callback function if AJAX request is successful
                window.location.href = ``
            },
            error: function (xhr, status, error) {
                // Handle error if AJAX request fails
                console.error("Error:", error);
            }
        });
    }

    function addAssumptionRow() {
        var newRowHtml = '<tr>' +
            '<td><input type="text" class="input" name="factor" placeholder="Enter Factor"></td>' +
            '<td><input type="text" class="input "  onblur="handleError($(this))" name="rate" placeholder="Enter Rate"></td>' +
            '<td><a class="button is-small is-danger-passive editBtn" type="button" data-target="assumptions" data-action="save">' +
            '<span class="icon"><i class="mdi mdi-plus"></i></span>' +
            '</a> <a class="button is-small is-danger-passive deleteBtn" type="button">' +
            '<span class="icon"><i class="mdi mdi-trash-can"></i></span>' +
            '</a></td>' +
            '</tr>';

        // Append the new row to the table
        $("#assumptions").append(newRowHtml);

        // Delegate click event for editBtn and deleteBtn within assumptions table
        $("#assumptions").on("click", ".editBtn", function () {
            // Your edit button logic here
        });


    }

    function addCurrencyRow() {
        var newRowHtml = '<tr>' +
            '<td><input type="text" class="input" name="currency" placeholder="Enter Currency"></td>' +
            '<td><input type="text" class="input "  onblur="handleError($(this))" name="rate" placeholder="Enter Rate"></td>' +
            '<td><a class="button is-small is-danger-passive editBtn" type="button" data-target="currency" data-action="save">' +
            '<span class="icon"><i class="mdi mdi-plus"></i></span>' +
            '</a> <a class="button is-small is-danger-passive deleteBtn" type="button">' +
            '<span class="icon"><i class="mdi mdi-trash-can"></i></span>' +
            '</a></td>' +
            '</tr>';

        // Append the new row to the table
        $("#currency_assumptions").append(newRowHtml);

        // Delegate click event for editBtn and deleteBtn within assumptions table
        $("#currency_assumptions").on("click", ".editBtn", function () {
            // Your edit button logic here
        });


    }

// Event listener for the "Add Row" button
    $("#addAssumptionRowBtn").click(function () {
        addAssumptionRow();
    });
    $("#addCurrencyRowBtn").click(function () {
        addCurrencyRow();
    });
    const expensesBtn = document.getElementById('expenseBtn')
    if (expensesBtn) {

        expensesBtn.addEventListener('click', ev => {
            ev.preventDefault()
            document.getElementById('expenses').classList.toggle('is-hidden')
        })
    }

    function handleClick(deptId) {
        return function (event) {
            event.preventDefault();
            const url = event.target.getAttribute('href');
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    updateTableAndPaginator(html, deptId);
                    addEventListenerToAnchorTag(deptId);
                });
        };
    }

    function addEventListenerToInputSearch(deptId) {
        console.log(deptId)
        const inputs = document.querySelectorAll(`[class*="input account-input-search-${deptId}"]`)
        console.log(inputs)
        if (inputs.length > 0) {
            inputs.forEach(input => {
                const fieldBody = input.closest('.modal');
                const criteriaSelect = fieldBody.querySelector('#search-criteria');
                const currentTableBody = fieldBody.querySelector('#table-body');
                criteriaSelect.addEventListener('change', (ev) => {
                    input.removeAttribute('disabled');
                    selectedFilter = ev.target.value;
                });
                input.addEventListener('input', (ev) => {
                    const val = ev.target.value.trim();
                    let deptartment = input.dataset.dept;

                    if (val === "") {
                        currentTableBody.innerHTML = "";
                        return;
                    }
                    // Fetch data based on search criteria
                    fetch(`/account/search?filter=${selectedFilter}&value=${val}&department=${deptartment}`)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(result => {
                            const data = result.data;
                            console.log(data)
                            currentTableBody.innerHTML = "";
                            data.forEach(acc => {
                                const row = document.createElement('tr');
                                row.setAttribute('role', 'row');
                                row.setAttribute('data-total', acc.total);

                                const accountIdCell = document.createElement('td');
                                accountIdCell.setAttribute('data-label', 'Account id');
                                accountIdCell.textContent = acc.account_id;
                                row.appendChild(accountIdCell);

                                const accountNameCell = document.createElement('td');
                                accountNameCell.setAttribute('data-label', 'Account name');
                                accountNameCell.textContent = acc.account__acctdesc;
                                row.appendChild(accountNameCell);

                                const actionsCell = document.createElement('td');
                                actionsCell.className = 'is-actions-cell';
                                const buttonsDiv = document.createElement('div');
                                buttonsDiv.className = 'buttons is-right';

                                const editButton = document.createElement('a');
                                editButton.className = 'button is-small is-light';
                                editButton.type = 'button';
                                editButton.href = acc.id ? `/update/${acc.id}` : '';
                                const editIcon = document.createElement('span');
                                editIcon.className = 'icon';
                                editIcon.innerHTML = '<i class="mdi mdi-file-edit"></i>';
                                editButton.appendChild(editIcon);

                                const deleteButton = document.createElement('a');
                                deleteButton.className = 'button is-small is-danger-passive';
                                deleteButton.type = 'button';
                                deleteButton.href = acc.id ? `/delete_budget/${acc.id}` : '';
                                deleteButton.setAttribute('data-target', 'sample-modal');
                                const deleteIcon = document.createElement('span');
                                deleteIcon.className = 'icon';
                                deleteIcon.innerHTML = '<i class="mdi mdi-trash-can"></i>';
                                deleteButton.appendChild(deleteIcon);

                                buttonsDiv.appendChild(editButton);
                                buttonsDiv.appendChild(deleteButton);
                                actionsCell.appendChild(buttonsDiv);
                                row.appendChild(actionsCell);

                                // Append more cells as needed

                                currentTableBody.appendChild(row);
                            });
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                });// Add the handleClick function as the event listener
            })

        } else {
        }
    }

    function addEventListenerToAnchorTag(deptId) {
        const paginationLinks = document.querySelectorAll(`[class*="custom-pagination-${deptId}"]`)
        console.log(paginationLinks)
        if (paginationLinks.length > 0) {
            paginationLinks.forEach(link => {
                link.addEventListener('click', handleClick(deptId)); // Add the handleClick function as the event listener
            });
        } else {
        }
    }

    function updateTableAndPaginator(html, deptId) {
        const parser = new DOMParser();
        const newDoc = parser.parseFromString(html, 'text/html');
        const newRow = newDoc.querySelectorAll(`#table-body-${deptId} tr`);
        const newTable = newDoc.getElementById(`table-body-${deptId}`);
        const newPaginator = newDoc.getElementById(`paginator-${deptId}`);
        document.getElementById(`table-body-${deptId}`).replaceWith(newTable);
        document.getElementById(`paginator-${deptId}`).replaceWith(newPaginator);

        // Add any other necessary post-update operations
    }

// Add the event listener to the first pagination link for each department
    const deptIds = ['CEO', 'Internal Audit', 'Supply Chain', 'Strategy', 'Public Relations', 'Technical', 'Information Systems', 'Legal & Risk', 'Human Capital', 'Sales & Marketing', 'Administration', 'Finance', 'Staff & Remunerations','Assets'];
    deptIds.forEach(deptId => {
        addEventListenerToAnchorTag(deptId);
        addEventListenerToInputSearch(deptId)

    });
});
