window.onload = (event) => {

    const facebookBtn = document.querySelector(".facebook-btn");
    const twitterBtn = document.querySelector(".twitter-btn");
    const linkedinBtn = document.querySelector(".linkedin-btn");
    const whatsappBtn = document.querySelector(".whatsapp-btn");

    let postUrl = encodeURI(document.location.href);
    let postTitle = encodeURI("Check this out: ");

    if (facebookBtn) {
        facebookBtn.setAttribute(
        "href",
        `https://www.facebook.com/sharer.php?u=${postUrl}`
        );
    }

    if (twitterBtn) {
        twitterBtn.setAttribute(
        "href",
        `https://twitter.com/share?url=${postUrl}&text=${postTitle}`
        );
    }

    if (linkedinBtn) {
        linkedinBtn.setAttribute(
        "href",
        `https://www.linkedin.com/shareArticle?url=${postUrl}&title=${postTitle}`
        );
    }

    if (whatsappBtn) {
        whatsappBtn.setAttribute(
        "href",
        `https://wa.me/?text=${postTitle} ${postUrl}`
        );
    }


    let mybutton = document.getElementById("btn-back-to-top");


    window.onscroll = function () {
      scrollFunction();
    };

    function scrollFunction() {
      if (
        document.body.scrollTop > 20 ||
        document.documentElement.scrollTop > 20
      ) {
        mybutton.style.display = "block";
      } else {
        mybutton.style.display = "none";
      }
    }

    mybutton.addEventListener("click", backToTop);

    function backToTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }

};

