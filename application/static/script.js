window.onload = (event) => {

    const facebookBtn = document.querySelector(".facebook-btn");
    const twitterBtn = document.querySelector(".twitter-btn");
    const linkedinBtn = document.querySelector(".linkedin-btn");
    const whatsappBtn = document.querySelector(".whatsapp-btn");

    let postUrl = encodeURI(document.location.href);
    let postTitle = encodeURI("Check this out: ");

    facebookBtn.setAttribute(
    "href",
    `https://www.facebook.com/sharer.php?u=${postUrl}`
    );

    twitterBtn.setAttribute(
    "href",
    `https://twitter.com/share?url=${postUrl}&text=${postTitle}`
    );

    linkedinBtn.setAttribute(
    "href",
    `https://www.linkedin.com/shareArticle?url=${postUrl}&title=${postTitle}`
    );

    whatsappBtn.setAttribute(
    "href",
    `https://wa.me/?text=${postTitle} ${postUrl}`
    );

};

