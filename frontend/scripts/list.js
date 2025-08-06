// Ensure jQuery is loaded before this script runs
window.BASE_URL = "https://more-urchin-hopeful.ngrok-free.app";

function startListPage() {
    const params = new URLSearchParams(window.location.search);
    const park = params.get('park');
    if (park) {
        mapping = {
            "disneyland": "Disneyland Resort",
            "california_adventure": "Disney's California Adventure",
            "food": "Seasonal Food at Disneyland and California Adventure"
        }
        document.body.insertAdjacentHTML('afterbegin', `<h2 class="list-header">${mapping[park]}</h2>`);
    }
}

function getListItems() {
    const params = new URLSearchParams(window.location.search);
    const park = params.get('park');
    fetch(`${window.BASE_URL}/checklist/${park}`, {
        "headers": {
            "ngrok-skip-browser-warning": true
        }
    }).then(response => response.json())
        .then(data => {
            const lands = {};
            Object.keys(data).forEach(rideKey => {
                const ride = data[rideKey];
                const land = ride.land || "Other";
                if (!lands[land]) {
                    lands[land] = [];
                }
                lands[land].push({ key: rideKey, ...ride });
            });

            Object.keys(lands).forEach(land => {
                $(".ride-list").append(`<h3 class="land-header">${land}</h3>`);
                lands[land].forEach(ride => {
                    $(".ride-list").append(
                        `<div class="checklist-item">
                    <div class="checkbox-wrapper-30">
                        <span class="checkbox">
                            <input type="checkbox" id="${ride.key}" ${ride.didRide ? "checked" : ""} />
                            <svg>
                                <use xlink:href="#checkbox-30" class="checkbox"></use>
                            </svg>
                        </span>
                        <svg xmlns="http://www.w3.org/2000/svg" style="display:none">
                            <symbol id="checkbox-30" viewBox="0 0 22 22">
                                <path fill="none" stroke="currentColor" d="M5.5,11.3L9,14.8L20.2,3.3l0,0c-0.5-1-1.5-1.8-2.7-1.8h-13c-1.7,0-3,1.3-3,3v13c0,1.7,1.3,3,3,3h13 c1.7,0,3-1.3,3-3v-13c0-0.4-0.1-0.8-0.3-1.2"/>
                            </symbol>
                        </svg>
                        <p class="ride-name">${ride.name}</p>
                    </div>
                </div>`
                    );
                });
            });
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('rideList');
    form.addEventListener('change', function (event) {
        event.preventDefault();
        const changedCheckbox = event.target;
        console.log('Changed item:', changedCheckbox.id, changedCheckbox.checked);
        submitChange(changedCheckbox)
    });
});

function submitChange(changedCheckbox) {
    const params = new URLSearchParams(window.location.search);
    const park = params.get('park');
    fetch(`${window.BASE_URL}/checklist/${park}/${changedCheckbox.id}`, {
        method: "PUT"
    });
}

function submitChecklist() {
    const params = new URLSearchParams(window.location.search);
    const park = params.get('park');
    const checked = $('.ride-list input[type="checkbox"]:checked');
    console.log(checked)
    const checkedIds = Array.from(checked).map(cb => cb.id);
    console.log('Checked ride IDs:', checkedIds);
    fetch(`${window.BASE_URL}/test`, {
        method: "POST",
        headers: {
            "ngrok-skip-browser-warning": true
        },
        body: JSON.stringify({
            "park": park,
            "checked": checkedIds
        })
    });
}
