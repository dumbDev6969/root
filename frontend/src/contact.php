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
        .social-icons a{
            color: #6C757D;
        }
    </style>
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container mt-5 p-5">
        <div class="row d-flex align-items-center jsutify-content-center">
            <div class="col-md-5">
                <div class="contact-info p-5 rounded bg-light" >
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
                <form class="row g-3 mt-3">
                    <!-- First Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="first-name" class="form-control" id="first-name-input" placeholder="First name" required>
                            <label for="first-name-input">First Name</label>
                        </div>
                    </div>
                    <!-- Last Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="last-name" class="form-control" id="last-name-input" placeholder="Last name" required>
                            <label for="last-name-input">Last Name</label>
                        </div>
                    </div>
                    <!-- Phone Number -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="number" name="phone" class="form-control" id="phone-number" placeholder="Phone #" min="0" required>
                            <label for="phone-number">Phone Number</label>
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
                    <button class="btn btn-dark" type="submit" style="height: 60px;">Send Message</button>
                </form>
            </div>
        </div>
    </div>
    <?php include '../includes/footer.php' ?>
</body>

</html>