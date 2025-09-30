
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("message-form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const message = document.getElementById("name").value;

        // If the form validation function returns true send the post request to the route in fetch
        if (validateForm(name, message)) {
            fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "Application/json"
                },
                body: JSON.stringify({
                    name: name,
                    message: message
                })
            })
            // If the server responds incorrectly throw an error
            .then(res => {
                if (!res.ok) {
                    throw new Error("Error submitting form");
                }
                return res.json();
            })
            .catch(err => {
                console.error(err);
            });          
        }
    });
});

const validateForm = (name, message) => {
    return true;
}