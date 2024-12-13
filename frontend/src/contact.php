<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>
        Contact Form
    </title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../assets/links.css">
    <style>
        .social-icons a {
            color: #6C757D;
        }
    </style>
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container mt-5 p-5">
        <div class="row d-flex align-items-center jsutify-content-center">
            <div class="col-md-5">
                <div class="contact-info p-5 rounded bg-light">
                    <h2>Get in touch</h2>
                    <div>
                        <strong>Chat to us</strong>

                        <p>Our friendly team is here to help.</p>
                        <a href="mailto:hello@paysphere.com">
                            sample@gmail.xom
                        </a>
                    </div>
                    <div>
                        <strong>
                            Call us
                        </strong>

                        <p>Mon-Fri from 8am to 8:01am</p>

                        <p>(+995) 555-55-55-55</p>
                    </div>
                    <p>
                        <strong>
                            Social media
                        </strong>
                    </p>
                    <div class="social-icons d-flex  w-25 justify-content-between">
                        <a href="#">
                            <i class="bi bi-facebook"></i>
                        </a>
                        <a href="#">
                            <i class="bi bi-github"></i>
                        </a>
                        <a href="#">
                            <i class="bi bi-twitter-x"></i>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-7">
                <form id="contactForm" class="row g-3 mt-3">
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="first_name" class="form-control" id="first-name-input" placeholder="First name" required>
                            <label for="first-name-input">First Name</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="last_name" class="form-control" id="last-name-input" placeholder="Last name" required>
                            <label for="last-name-input">Last Name</label>
                        </div>
                    </div>

                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="email" name="email" class="form-control" id="email" placeholder="Email" required>
                            <label for="email">Email</label>
                        </div>
                    </div>

                    <div class="col-md-12">
                        <textarea class="form-control" name="message" id="messsage-input" placeholder="Message" max="200"></textarea>
                    </div>
                    <div class="col-md-12 ">
                        <input class="form-check-input" id="privacyPolicy" type="checkbox" />
                        <label class="form-check-label" for="privacyPolicy">
                            I'd like to receive more information about company. I understand and agree to the
                            <a class="text-primary" href="#">
                                Privacy Policy
                            </a>
                        </label>
                    </div>
                </form>
                <button class="btn btn-dark" type="button" onclick="submitForm()" style="height: 60px;">Send Message</button>
                <script>
                    function submitForm() {
                        alert("submitting form");
                        const form = document.getElementById('contactForm');
                        const formData = new FormData(form);
                        const jsonData = {};
                        formData.forEach((value, key) => {
                            jsonData[key] = value;
                        });
                        console.log('JSON data:', jsonData);

                        fetch('http://127.0.0.1:11352/contact_sendmail', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(jsonData),
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log('Success:', data);
                            })
                            .catch((error) => {
                                console.error('Error:', error);
                            });
                    }
                </script>
            </div>
        </div>
    </div>
    <?php include '../includes/footer.php' ?>
</body>

</html>