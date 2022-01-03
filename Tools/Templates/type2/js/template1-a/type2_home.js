'use strict';

if ( location.hash ) {
	var currentSection = document.querySelector(location.hash);
}
else {
	var currentSection;
}
var header = document.querySelector('header');
var navbarLogo = document.querySelector('.navbar-logo');
var navbarBrand = document.querySelector('.navbar-brand');
var navItems = document.querySelectorAll('.nav-item');
var navbarToggler = document.querySelectorAll('.navbar-toggler')[0];
var navbarCollapse = document.querySelector('.navbar-collapse');
var navbarNav = document.querySelector('.navbar-nav');
var headerLinksArray = Array.prototype.slice.call(document.querySelectorAll('header a'));
var sectionNextArray = Array.prototype.slice.call(document.querySelectorAll('.section-next'));
var introNext = document.querySelector('#intro-next');

var introIsClicked = false;
var aboutIsClicked = false;
var servicesIsClicked = false;
var portfolioIsClicked = false;
var contactIsClicked = false;
var navLinks = document.querySelectorAll('.nav-link');

var isNewScroll = false;

function scrollToElement(toElement) {
	var itCount = 0;
	isNewScroll = true;
	var scrollAnim = setInterval( function () {
	if ( itCount <= 2 || itCount > 2 && isNewScroll === false ) {
		if ( window.pageYOffset !== toElement.offsetTop && Math.abs(toElement.offsetTop - window.pageYOffset) > 100 ) {
			window.scroll(0, (window.pageYOffset + (toElement.offsetTop-window.pageYOffset)/10));
		}
		else if ( window.pageYOffset !== toElement.offsetTop && Math.abs(toElement.offsetTop - window.pageYOffset) > 50 ) {
		    window.scroll(0, (window.pageYOffset + (toElement.offsetTop-window.pageYOffset)/8));
		}
		else if ( window.pageYOffset !== toElement.offsetTop && Math.abs(toElement.offsetTop - window.pageYOffset) > 30 ) {
		    window.scroll(0, (window.pageYOffset + (toElement.offsetTop-window.pageYOffset)/6));
		}
		else if ( window.pageYOffset !== toElement.offsetTop && Math.abs(toElement.offsetTop - window.pageYOffset) > 5 ) {
		    window.scroll(0, (window.pageYOffset + (toElement.offsetTop-window.pageYOffset)/4));
		}
		else {
			window.scroll( 0, toElement.offsetTop );
			clearInterval(scrollAnim);
		}
	}
	else {
		clearInterval(scrollAnim);
	}
	itCount += 1;
	if ( itCount >= 2 ) {
		isNewScroll = false;
	}
	}, 17);
}


headerLinksArray.forEach(link => {
	link.addEventListener('click', function (event) {
		if (!('scrollBehavior' in document.documentElement.style)) {
			event.preventDefault();
			scrollToElement(document.getElementById(this.getAttribute('href').slice(1)));
		}
		if ( isDroppedDown ) {
			dropdownFormat();
		}
		if ( headerLinksArray.indexOf(this) === 0 ) {
			history.replaceState(undefined, undefined, '#intro');
			introIsClicked = true;
			setTimeout( function () {
				introIsClicked = false;
			}, 625);
		}
		else if ( headerLinksArray.indexOf(this) === 1 ) {
			history.replaceState(undefined, undefined, '#about');
			aboutIsClicked = true;
			setTimeout( function () {
				aboutIsClicked = false;
			}, 625);
		}
		else if ( headerLinksArray.indexOf(this) == 2 ) {
			history.replaceState(undefined, undefined, '#services');
			servicesIsClicked = true;
			setTimeout( function () {
				servicesIsClicked = false;
			}, 625);
		}
		else if ( headerLinksArray.indexOf(this) == 3 ) {
			history.replaceState(undefined, undefined, '#portfolio');
			portfolioIsClicked = true;
			setTimeout( function () {
				portfolioIsClicked = false;
			}, 625);
		}
		else if ( headerLinksArray.indexOf(this) == 4 ) {
			history.replaceState(undefined, undefined, '#contact');
			contactIsClicked = true;
			setTimeout( function () {
				contactIsClicked = false;
			}, 625);
		}
	});
});

introNext.addEventListener('click', function (event) {
	if (!('scrollBehavior' in document.documentElement.style)) {
		event.preventDefault();
		scrollToElement(aboutDiv);
	}
	history.replaceState(undefined, undefined, '#about');
});

sectionNextArray.forEach(link => {
	link.addEventListener('click', function (event) {
		if (!('scrollBehavior' in document.documentElement.style)) {
			event.preventDefault();
			scrollToElement(document.getElementById(this.getAttribute('href').slice(1)));
		}										// Added 02/07/2020
		if ( sectionNextArray.indexOf(this) === 0 ) {
			history.replaceState(undefined, undefined, '#services');
			servicesIsClicked = true;
			setTimeout( function () {
				servicesIsClicked = false;
			}, 625);
		}
		else if ( sectionNextArray.indexOf(this) === 1 ) {
			history.replaceState(undefined, undefined, '#portfolio');
			portfolioIsClicked = true;
			setTimeout( function () {
				portfolioIsClicked = false;
			}, 625);
		}
		else if ( sectionNextArray.indexOf(this) == 2 ) {
			history.replaceState(undefined, undefined, '#contact');
			contactIsClicked = true;
			setTimeout( function () {
				contactIsClicked = false;
			}, 625);
		}
	});
});

function navbarFormat() {
	// If page is scrolled down from top
	if ( window.pageYOffset >= header.offsetHeight ) {
		navbarLogo.style.height = headerHeightSmall * .8 + 'em';
		navbarBrand.style.fontSize = '175%';
		navbarBrand.style.left = '55px';
		navbarBrand.style.transform = 'translate(0%, -50%)';
		header.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
		header.style.height = headerHeightSmall + 'em';
		navbarLogo.style.filter = 'invert(0%)';
		navbarToggler.style.filter = 'invert(0%)';
		navbarBrand.style.color = '#bbb';

		// (min-width: 1200px)
		if ( window.innerWidth > breakpointWidthL ) {
			navbarLogo.style.height = headerHeightSmall * .8 + 'em';
			navbarBrand.style.fontSize = '175%';
			navbarBrand.style.left = '55px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'none';
			navbarCollapse.style.display = 'inline-block';
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			navbarCollapse.style.height = 'auto';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '14vw';
				navItem.style.marginRight = '1vw';
			}
		}
		// (min-width: 992px)
		else if ( window.innerWidth > breakpointWidthM ) {
			navbarLogo.style.height = headerHeightSmall * .8 + 'em';
			navbarBrand.style.fontSize = '175%';
			navbarBrand.style.left = '55px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'none';
			navbarCollapse.style.display = 'inline-block';
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			navbarCollapse.style.height = 'auto';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '7vw';
				navItem.style.marginRight = '1vw';
			}
		}
		// (min-width: 768px)
		else if ( window.innerWidth > breakpointWidthS ) {
			navbarLogo.style.height = headerHeightSmall * .8 + 'em';
			navbarBrand.style.fontSize = 'calc(9px + 2vw)';
			navbarBrand.style.left = '55px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'none';
			navbarCollapse.style.display = 'inline-block';
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			navbarCollapse.style.height = 'auto';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '7vw';
				navItem.style.marginRight = '1vw';
			}
			
		}
		// (min-width: 576px)
		else if ( window.innerWidth > breakpointWidthXS ) {
			navbarLogo.style.height = headerHeightSmall * .8 + 'em';
			navbarBrand.style.fontSize = 'calc(10px + 3vw)';
			navbarBrand.style.left = '55px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'inline-block';
			if ( !isDroppedDown ) {
				navbarCollapse.style.display = 'none';
				header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			}
			else {
				header.style.transition = 'height 0s, background-color 0s';
			}
			navbarCollapse.style.top = headerHeightSmall + 'em';
			navbarCollapse.style.transform = 'translate(-50%, 0%)';
			navbarCollapse.style.left = '50%';
			navbarCollapse.style.width = '101%';
			navbarCollapse.style.textAlign = 'center';
			navbarCollapse.style.backgroundColor = 'rgba(25, 25, 25, 0.9)';
			navbarCollapse.style.height = navbarNav.offsetHeight + 'px';
			isDroppedDown = false;
			for ( let navItem of navItems ) {
				navItem.style.display = 'block';
				navItem.style.paddingTop = '0.875em';
				navItem.style.paddingBottom = '0.875em';
				navItem.style.marginLeft = '0';
				navItem.style.marginRight = '0';
			}
		}
		// (max-width: 576px)
		else {
			header.style.height = 0.85 * headerHeightSmall + 'em';
			navbarLogo.style.height = headerHeightSmall * .6 + 'em';
			navbarBrand.style.fontSize = 'calc(10px + 3vw)';
			navbarBrand.style.left = '50%';
			navbarBrand.style.transform = 'translate(-50%, -50%)';
			navbarToggler.style.display = 'inline-block';
			if ( !isDroppedDown ) {
				navbarCollapse.style.display = 'none';
				header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			}
			else {
				header.style.transition = 'height 0s, background-color 0s';
			}
			navbarCollapse.style.top = headerHeightSmall * 0.85 + 'em';
			navbarCollapse.style.transform = 'translate(-50%, 0%)';
			navbarCollapse.style.left = '50%';
			navbarCollapse.style.width = '101%';
			navbarCollapse.style.textAlign = 'center';
			navbarCollapse.style.backgroundColor = 'rgba(25, 25, 25, 0.9)';
			navbarCollapse.style.height = navbarNav.offsetHeight + 'px';
			for ( let navItem of navItems ) {
				navItem.style.display = 'block';
				navItem.style.paddingTop = '0.875em';
				navItem.style.paddingBottom = '0.875em';
				navItem.style.marginLeft = '0';
				navItem.style.marginRight = '0';
			}
		}
	}

	// If at top of page
	else {
		header.style.backgroundColor = 'rgba(0, 0, 0, 0.0)';
		navbarLogo.style.filter = 'invert(100%)';
		navbarToggler.style.filter = 'invert(100%)';
		navbarBrand.style.color = '#191919';
		header.style.height = headerHeightLarge + 'em';
		navbarToggler.style.display = 'none';
		for ( let navItem of navItems ) {
			navItem.style.borderColor = 'black';
			navItem.style.color = '#bbb';
		}
		// (min-width: 1200px)
		if ( window.innerWidth > breakpointWidthL ) {
			navbarBrand.style.fontSize = '250%';
			navbarBrand.style.left = '50%';
			navbarBrand.style.transform = 'translate(-50%, -50%)';
			navbarToggler.style.display = 'none';
			navbarLogo.style.height = headerHeightLarge * .8 + 'em';
			navbarCollapse.style.display = 'inline-block';
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.height = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '1vw';
				navItem.style.marginRight = '1vw';
				navItem.style.fontSize = '100%';
				navItem.style.color = '#191919';
			}
		}
		// (min-width: 992px)
		else if ( window.innerWidth > breakpointWidthM ) {
			navbarBrand.style.fontSize = '250%';
			navbarBrand.style.left = '80px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'none';
			navbarLogo.style.height = headerHeightLarge * .8 + 'em';
			navbarCollapse.style.display = 'inline-block';			
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.height = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '1vw';
				navItem.style.marginRight = '1vw';
				navItem.style.fontSize = '100%';
				navItem.style.color = '#191919';
			}
		}
		// (min-width: 768px)
		else if ( window.innerWidth > breakpointWidthS ) {
			navbarLogo.style.height = headerHeightLarge * .8 + 'em';
			navbarBrand.style.fontSize = 'calc(9px + 3vw)';
			navbarBrand.style.left = '80px';
			navbarBrand.style.transform = 'translate(0%, -50%)';
			navbarToggler.style.display = 'none';
			navbarCollapse.style.display = 'inline-block';
			navbarCollapse.style.left = '100%';
			navbarCollapse.style.transform = 'translate(-100%, -50%)';
			navbarCollapse.style.top = '50%';
			navbarCollapse.style.textAlign = 'right';
			navbarCollapse.style.width = 'auto';
			navbarCollapse.style.height = 'auto';
			navbarCollapse.style.backgroundColor = 'rgba(0, 0, 0, 0)';
			isDroppedDown = false;
			header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '2vw';
				navItem.style.marginRight = '1vw';
				navItem.style.fontSize = '100%';
				navItem.style.color = '#191919';
			}
		}
		// (min-width: 576px)
		else if ( window.innerWidth > breakpointWidthXS ) {
			navbarLogo.style.height = headerHeightLarge * .65 + 'em';
			navbarBrand.style.fontSize = 'calc(10px + 3vw)';
			navbarBrand.style.left = '50%';
			navbarBrand.style.transform = 'translate(-50%, -50%)';
			navbarToggler.style.display = 'inline-block';
			if ( !isDroppedDown ) {
				navbarCollapse.style.display = 'none';
				header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			}
			else {
				header.style.transition = 'height 0s, background-color 0s';
			}
			navbarCollapse.style.top = headerHeightLarge + 'em';
			navbarCollapse.style.transform = 'translate(-50%, 0%)';
			navbarCollapse.style.left = '50%';
			navbarCollapse.style.width = '100%';
			navbarCollapse.style.textAlign = 'center';
			navbarCollapse.style.backgroundColor = 'rgba(25, 25, 25, 0)';
			for ( let navItem of navItems ) {
				navItem.style.display = 'inline-block';
				navItem.style.marginLeft = '6vw';
				navItem.style.marginRight = '6vw';
				navItem.style.fontSize = '100%';
				navItem.style.color = '#191919';
			}
		}
		// (max-width: 576px)
		else {
			navbarLogo.style.height = headerHeightSmall * .6 + 'em';
			navbarBrand.style.fontSize = 'calc(10px + 3vw)';
			navbarBrand.style.left = '50%';
			navbarBrand.style.transform = 'translate(-50%, -50%)';
			navbarToggler.style.display = 'inline-block';
			if  ( !isDroppedDown ) {
				navbarCollapse.style.display = 'none';
				header.style.transition = 'height 0.375s ease, background-color 0.375s ease';
			}
			else {
				header.style.transition = 'height 0s, background-color 0s';
			}
			navbarCollapse.style.top = headerHeightLarge * 0.85 + 'em';
			navbarCollapse.style.transform = 'translate(-50%, 0%)';
			navbarCollapse.style.left = '50%';
			navbarCollapse.style.width = '101%';
			navbarCollapse.style.textAlign = 'center';
			navbarCollapse.style.backgroundColor = 'rgba(25, 25, 25, 0.8)';
			navbarCollapse.style.height = navbarNav.offsetHeight + 'px';
			for ( let navItem of navItems ) {
				navItem.style.display = 'block';
				navItem.style.paddingTop = '0.875em';
				navItem.style.paddingBottom = '0.875em';
				navItem.style.marginLeft = '0';
				navItem.style.marginRight = '0';
				setTimeout( function () { 
					navItem.style.color = '#bbb';
				}, 10);
			}
		}
	}
}

// Change header parameters depending on scroll position
window.addEventListener('scroll', function () {
	navbarFormat();
});

var isDroppedDown = false;

function dropdownFormat() {
	if ( navbarCollapse.style.display == 'none' ) {
		navbarCollapse.style.display = 'inline-block';
		navbarCollapse.style.height = '0';
		setTimeout(function () {
			navbarCollapse.style.height = navbarNav.offsetHeight + 'px';
		}, 20);
		isDroppedDown = true;
	}
	else {
		setTimeout(function () {
			navbarCollapse.style.height = '0px';
		}, 20);
		setTimeout(function () {
			navbarCollapse.style.display = 'none';
			isDroppedDown = false;
		}, 300);
	}
}

navbarToggler.addEventListener('click', dropdownFormat);

var servicesColumns = document.querySelectorAll('.services-column');
var servicesColumnsArray = Array.prototype.slice.call(servicesColumns);
var servicesBlurbsFull = document.querySelectorAll('.blurb-full');
var servicesCards = document.querySelectorAll('.services-card');
var servicesBlurbsMobile = document.querySelectorAll('.blurb-mobile');
var servicesFullSpans = document.querySelectorAll('.blurb-full span');
var fullSpansArray = Array.prototype.slice.call(servicesFullSpans);
var servicesMobileSpans = document.querySelectorAll('.blurb-mobile span');
var mobileSpansArray = Array.prototype.slice.call(servicesMobileSpans);

mobileSpansArray.forEach(span => {
	span.addEventListener('click', function () {
		var currentSpan = mobileSpansArray.indexOf(this);
		for ( let card of servicesCards ) {
			card.style.opacity = '0';
			setTimeout(function () {
					card.style.display = 'none';
				}, 375);
			if  ( card == servicesCards[currentSpan] ) {
				setTimeout(function () {
					card.style.opacity = '1';
					card.style.display = 'inline-block';
				}, 500);
			}
		}

		setTimeout( function () {
			servicesBlurbsMobile[currentSpan].style.display = 'none';
		}, 375);
		setTimeout( function () {
			for ( let column of servicesColumnsArray ) {
				if ( currentSpan / 2 < servicesColumnsArray.indexOf(column) || currentSpan >= 2 && servicesColumnsArray.indexOf(column) === 0 ) {
					column.style.display = 'none';
				}
			}
			servicesBlurbsFull[currentSpan].style.display = 'inline-block';
			servicesFullSpans[currentSpan].style.display = 'inline-block';
		}, 500);
		isFullServices = true;
	});
});

function servicesFullRestore() {
	for ( let mobileBlurb of servicesBlurbsMobile ) {
		mobileBlurb.style.display = 'none';
	}
	for ( let column of servicesColumns ) {
		column.style.display = 'inline-block';
		}
	for ( let card of servicesCards ) {
		card.style.display = 'inline-block';
		card.style.opacity = '1';
	}
	for ( let fullBlurb of servicesBlurbsFull ) {
		fullBlurb.style.display = 'inline-block';
	}
	for ( let fullSpan of servicesFullSpans ) {
		fullSpan.style.display = 'none';
	}
}

function servicesMobileRestore() {
	for ( let mobileBlurb of servicesBlurbsMobile ) {
		mobileBlurb.style.display = 'inline-block';
	}
	for ( let fullBlurb of servicesBlurbsFull ) {
		fullBlurb.style.display = 'none';
	}
}

fullSpansArray.forEach(span => {
	span.addEventListener('click', function () {
		var currentSpan = fullSpansArray.indexOf(this);
		for ( let card of servicesCards ) {
				card.style.opacity = '0';
		}
		setTimeout( function () {
			for ( let column of servicesColumns ) {
				column.style.display = 'inline-block';
			}
			for ( let card of servicesCards ) {
				card.style.display = 'inline-block';
				card.style.opacity = '1';
			}
			servicesBlurbsMobile[currentSpan].style.display = 'inline-block';
			servicesBlurbsFull[currentSpan].style.display = 'none';
			servicesFullSpans[currentSpan].style.display = 'none';
		}, 500);
		isFullServices = false;
	});
	
});

var overlay = document.querySelector('#overlay');
var portfolioSlideshow = document.querySelector('.portfolio-slideshow');
var slideshowImgs = document.querySelectorAll('.slideshow-img');
var slideshowImgContainer = document.getElementById('slideshow-img-container');
var slideshowImgBackings = document.querySelectorAll('.slideshow-img-backing');
var slideshowControls = document.querySelectorAll('.slideshow-controls');
var exitSlideshowButton = document.querySelector('#exit-slideshow');
var panels = document.querySelectorAll('.portfolio-panel');
var panelsArray = Array.prototype.slice.call(panels);
var panelImgs = document.querySelectorAll('.panel-img');


var contactDiv = document.getElementById('contact');
var portfolioDiv = document.getElementById('portfolio');
var servicesDiv = document.getElementById('services');
var aboutDiv = document.getElementById('about');

var breakpointHeight = 600; // "px" units

var breakpointWidthXS = 576; // "px" units
var breakpointWidthS = 768;
var breakpointWidthM = 992;
var breakpointWidthL = 1200;

var scrollToTop = false;

var headerHeightLarge = 5; // "em" units
var headerHeightSmall = 3; // "em" units

var isFullServices = false;

var prevScreenWidth = window.innerWidth;

window.addEventListener('resize', function () {
	// currentSection.scrollIntoView();									/* Changed 2020128 */
	navbarFormat();
	if ( window.innerWidth > 576 )  {
		servicesFullRestore();
		isFullServices = false;
	}
	else if ( window.innerWidth <= 576 && !isFullServices ){
		servicesMobileRestore();
	}
	navItemHighlight();

	// Reformat the slideshow but only if a breakpoint is crossed									/* Added 01/28/2020 */
	/*if ( window.innerWidth <= breakpointWidthXS && prevScreenWidth > breakPointWidthXS ) {
		portfolioFormat();
	}
	else if ( window.innerWidth > breakPointWidthXS && prevScreenWidth <= breakpointWidthXS ) {
		portfolioFormat();
	}
	else if ( window.innerWidth <= breakpointWidthS && prevScreenWidth > breakpointWidthS ) {
		portfolioFormat();
	}
	else if ( window.innerWidth > breakpointWidthS && prevScreenWidth <= breakpointWidthS ) {
		portfolioFormat();
	}
	else if ( window.innerWidth <= breakpointWidthM && prevScreenWidth > breakpointWidthM ) {
		portfolioFormat();
	}
	else if ( window.innerWidth > breakpointWidthM && prevScreenWidth <= breakpointWidthM ) {
		portfolioFormat();
	}
	else if ( window.innerWidth <= breakpointWidthL && prevScreenWidth > breakpointWidthL ) {
		portfolioFormat();
	}
	else if ( window.innerWidth > breakpointWidthL && prevScreenWidth <= breakpointWidthL ) {
		portfolioFormat();
	}*/
	portfolioFormat();																			/* Removed 01/28/2020 */
	if ( portfolioSlideshow.style.display !== 'none' ) {
		positionSlideshow();
	}
	prevScreenWidth = window.innerWidth;
});

function navItemHighlight() {
	if ( window.pageYOffset >= contactDiv.offsetTop - contactDiv.offsetHeight / 2 /* - header.offsetHeight */ ) {
		setTimeout( function () {
			if ( location.hash == '#contact' && contactIsClicked ){
				history.replaceState(undefined, undefined, '#contact');
			}
			else if ( !portfolioIsClicked && !servicesIsClicked && !aboutIsClicked && !introIsClicked ) {
				history.replaceState(undefined, undefined, '#contact');
			}
		}, 375);
		for ( let section of navItems ) {
			if ( section.getAttribute('href') != '#contact') {
				section.style.color = '#888';
			}
			else {
				section.style.color = 'white';
			}
		}
	}
	else if ( window.pageYOffset >= portfolioDiv.offsetTop - portfolioDiv.offsetHeight / 2 && window.pageYOffset < contactDiv.offsetTop - contactDiv.offsetHeight / 2 /* - header.offsetHeight */  /* contactDiv.offsetTop - header.offsetHeight */  ) {
		setTimeout( function () {
			if ( location.hash == '#portfolio' && portfolioIsClicked ) {
				history.replaceState(undefined, undefined, '#portfolio');
			}
			else if ( !contactIsClicked && !servicesIsClicked && !aboutIsClicked && ! introIsClicked ) {
				history.replaceState(undefined, undefined, '#portfolio');
			}
		}, 375);
		for ( let section2 of navItems ) {
			if ( section2.getAttribute('href') != '#portfolio') {
				section2.style.color = '#888';
			}
			else {
				section2.style.color = 'white';
			}
		}
	}
	else if ( window.pageYOffset >= servicesDiv.offsetTop - servicesDiv.offsetHeight / 2 && window.pageYOffset < portfolioDiv.offsetTop - portfolioDiv.offsetHeight / 2 /* header.offsetHeight */ /* portfolioDiv.offsetTop - header.offsetHeight */ ) {
		setTimeout( function () {
			if ( location.hash == '#services' && servicesIsClicked ) {
				history.replaceState(undefined, undefined, '#services');
			}
			else if ( !aboutIsClicked && !portfolioIsClicked && !contactIsClicked && !introIsClicked ) {
				history.replaceState(undefined, undefined, '#services');
			}
		}, 375);
		for ( let section3 of navItems ) {
			if ( section3.getAttribute('href') != '#services') {
				section3.style.color = '#888';
			}
			else {
				section3.style.color = 'white';
			}
		}
	}
	else if ( window.pageYOffset >= aboutDiv.offsetTop - aboutDiv.offsetHeight / 2 && window.pageYOffset < servicesDiv.offsetTop - servicesDiv.offsetHeight / 2 /* header.offsetHeight */  /* servicesDiv.offsetTop - header.offsetHeight */ ) {
		setTimeout( function () {
			if ( location.hash == '#about' && aboutIsClicked ) {
				history.replaceState(undefined, undefined, '#about');
			}
			else if ( !contactIsClicked && !portfolioIsClicked && !servicesIsClicked && !introIsClicked ) {
				history.replaceState(undefined, undefined, '#about');
			}
		}, 375);
		for ( let section4 of navItems ) {
			if ( section4.getAttribute('href') != '#about') {
				section4.style.color = '#888';
			}
			else {
				section4.style.color = 'white';
			}
		}
	}
	else {
		setTimeout( function () {
			if ( location.hash == '#intro' && introIsClicked ) {
				history.replaceState(undefined, undefined, '#intro');
			}
			else if ( !aboutIsClicked && !servicesIsClicked && !portfolioIsClicked && !contactIsClicked ) {
				history.replaceState(undefined, undefined, '#intro');
			}
		}, 375);
		for ( let section5 of navItems ) {
			if ( window.pageYOffset >= header.offsetHeight && !scrollToTop ) {
				section5.style.color = '#888';
			}
			else {
				section5.style.color = '#191919';
			}
		}
	}
}

window.addEventListener('scroll', function() { 
	navItemHighlight();
	currentSection = document.querySelector(location.hash);
});

var currentImg = 0;

function slideshowImgFormat() {
	for ( let i = 0; i < slideshowImgs.length; i++ ) {
		if ( i != currentImg ) {
			slideshowImgs[i].style.opacity = '0.375';
		}
		else {
			slideshowImgs[i].style.opacity = '1';
		}
	}
	for ( let i = 0; i < slideshowTexts.length; i++ ) {
		if ( i != currentImg ) {
			slideshowTexts[i].style.opacity = '0';
			slideshowBlurbs[i].style.opacity = '0';						// Added 01/31/2020
			slideshowBlurbs[i].style.display = '';
			slideshowTexts[i].style.borderRadius = '0';
			slideshowTexts[i].style.height = 'auto';
			slideshowTexts[i].style.top = '100%';
			slideshowTexts[i].style.left = '0';
			slideshowTexts[i].style.width = 'auto';
			slideshowTexts[i].style.transform = 'translate(0%, -100%)';
			slideshowTextToggleArray[i].innerHTML = 'more';
		}
		else {
			slideshowTexts[i].style.opacity = '1';
		}
	}
}

function positionSlideshow() {
	var slideshowImgContainerOffsetPercent = (( slideshowImgBackings[1].offsetLeft - slideshowImgBackings[0].offsetLeft - ( slideshowImgBackings[1].offsetLeft - slideshowImgBackings[0].offsetWidth ) / 4 ) / slideshowImgBackings[0].offsetWidth ) * 100;
	var imgPosition = currentImg * slideshowImgContainerOffsetPercent;
	slideshowImgContainer.style.transform = 'translate(-' + imgPosition + '%, 0%)';
}

panelsArray.forEach(panel => {
	panel.addEventListener('click', function () {
		if ( overlay.style.display != 'block' ) {
			isActiveSlideshowOverlay = true;
			currentImg = panelsArray.indexOf(this);
			overlay.style.display = 'block';
			overlay.style.backgroundColor = 'rgba(0,0,0,0)';
			slideshowImgContainer.style.transition = 'none';
			portfolioSlideshow.style.display = 'block';
			exitSlideshowButton.style.display = 'block';
			for ( let text of slideshowTexts ) {
				if ( text !== slideshowTexts[currentImg]) {
					text.style.opacity = '0';
				}
			}
			/*
			if ( window.innerHeight > breakpointHeight ) {
				portfolioSlideshow.style.width = 'calc(85vh * (4/3))';
			}
			else {
				portfolioSlideshow.style.width = 'calc(' + breakpointHeight + 'px * 0.85 * (4/3))';
			}*/
			//portfolioSlideshow.style.height = '0';
			positionSlideshow();
			setTimeout( function () { 
				overlay.style.backgroundColor = 'rgba(0,0,0,0.625)';/*
				if ( window.innerHeight > breakpointHeight ) {
					portfolioSlideshow.style.height = '85vh';
				}
				else {
					portfolioSlideshow.style.height = 'calc(0.85 * ' + breakpointHeight + 'px)';
				}*/
				for ( let backing of slideshowImgBackings ) {
					backing.style.opacity = '1';
				}
				/*
				for ( let img of slideshowImgs ) {
					img.style.height = '100%';
				}*/
			}, 0);
			setTimeout( function () {
				slideshowImgFormat();
				for ( let control of slideshowControls ) {
					control.style.opacity = '1';
				}
				exitSlideshowButton.style.opacity = '1';
				slideshowImgContainer.style.transition = 'transform 0.5s ease';
			}, 375);
		}
	});
});

var slideshowPrev = document.getElementById('slideshow-prev');
var slideshowNext = document.getElementById('slideshow-next');


slideshowNext.addEventListener('click', function () { 
	if ( currentImg < slideshowImgs.length - 1 ) {
		currentImg += 1;
		//positionSlideshow();
		/*
		let imgPosition = currentImg * 100.4;
		slideshowImgContainer.style.transform = 'translate(-' + imgPosition + '%, 0%)';
	*/}
	else {
		currentImg = 0;
		//positionSlideshow();
		//slideshowImgContainer.style.transform = 'translate(0%, 0%)';
	}
	positionSlideshow();
	slideshowImgFormat();
	portfolioFormat();
});

slideshowPrev.addEventListener('click', function () {
	if ( currentImg > 0 ) {
		currentImg -= 1;
		/*var imgPosition = currentImg * 100.5;
		slideshowImgContainer.style.transform = 'translate(-' + imgPosition + '%, 0%)';
	*/}
	else {
		currentImg = slideshowImgs.length - 1;
		/*imgPosition = currentImg * 100.5;
		slideshowImgContainer.style.transform = 'translate(-' + imgPosition + '%, 0%)';
	*/}
	positionSlideshow();
	slideshowImgFormat();
	portfolioFormat();
});

// Close slideshow when user clicks off of it.

function closeSlideshow() {
	isActiveSlideshowOverlay = false;
	overlay.style.backgroundColor = 'rgba(0,0,0,0)';
	for ( let img of slideshowImgs ) {
		img.style.transition = 'opacity 0.25s';
	}
	setTimeout( function () {
		for ( let img of slideshowImgs ) {
			img.style.opacity = '0'
		}
		for ( let control of slideshowControls ) {
			control.style.opacity = '0';
		}
		for ( let text of slideshowTexts ) {
			text.style.opacity = '0';
		}
		exitSlideshowButton.style.opacity = '0';
	}, 1);
	setTimeout( function () {
		for ( let backing of slideshowImgBackings ) {
			backing.style.opacity = '0';
		}
	}, 375);
	setTimeout( function () { 
		overlay.style.display = 'none';
		portfolioSlideshow.style.display = 'none';
		exitSlideshowButton.style.display = 'none';
	}, 625);
	for ( let img of slideshowImgs ) {
		img.style.transition = 'opacity 0.5s';
	}
}

overlay.addEventListener('click', function () {
	closeSlideshow();
});

exitSlideshowButton.addEventListener('click', function() {
	closeSlideshow();
});

var slideshowTextToggleArray = Array.prototype.slice.call(document.querySelectorAll('.slideshow-text-toggle'));
var slideshowBlurbs = document.querySelectorAll('.slideshow-blurb');
var slideshowTexts = document.querySelectorAll('.slideshow-text');

slideshowTextToggleArray.forEach(toggle =>  {
	toggle.addEventListener('click', function() {
		let index = slideshowTextToggleArray.indexOf(this);
		if ( slideshowBlurbs[index].style.display == 'none' || slideshowBlurbs[index].style.display == '') {
			slideshowBlurbs[index].style.display = 'inline-block';
			slideshowBlurbs[index].style.opacity = '1';
			slideshowTexts[index].style.borderRadius = '5px';
			slideshowTexts[index].style.top = '50%';
			slideshowTexts[index].style.left = '50%';
			slideshowTexts[index].style.width = '75%';
			slideshowTexts[index].style.transform = 'translate(-50%, -50%)';
			this.innerHTML = 'less';
		}
		else {
			slideshowBlurbs[index].style.opacity = '0';
			slideshowBlurbs[index].style.display = '';
			slideshowTexts[index].style.borderRadius = '0';
			slideshowTexts[index].style.height = 'auto';
			slideshowTexts[index].style.top = '100%';
			slideshowTexts[index].style.left = '0';
			slideshowTexts[index].style.width = 'auto';
			slideshowTexts[index].style.transform = 'translate(0%, -100%)';
			this.innerHTML = 'more';
		}
	});
});

slideshowTexts.forEach(text => {
	text.addEventListener('mouseover', function () {
		if ( window.innerWidth > breakpointWidthS ) {
			text.style.opacity = '0';
		}
	});
});

slideshowTexts.forEach(text => {
	text.addEventListener('mouseleave', function () {
		text.style.opacity = '1';
	});
});

var isActiveSlideshowOverlay = false;
var portfolioTitle = document.querySelector('#portfolio-title');
var portfolioNext = document.querySelector('#portfolio-next');
// var isSlideshowAdjusted = false;

function portfolioFormat() {
	if ( window.innerWidth > 768 ) {
		portfolioTitle.style.visibility = 'visible';
		portfolioNext.style.visibility = 'visible';
		portfolioSlideshow.style.top = '50%';
		portfolioSlideshow.style.height = '85vh';
		portfolioSlideshow.style.width = 'calc(85vh * (4/3))';
		if ( !isActiveSlideshowOverlay ) {
			portfolioSlideshow.style.display = 'none';
			for ( let img of slideshowImgs ) {
				img.style.opacity = '0';
			}
			for ( let backing of slideshowImgBackings ) {
				backing.style.opacity = '0';
			}
			for ( let control of slideshowControls ) {
				control.style.opacity = '0';
			}
		}
		for ( let text of slideshowTexts ) {
			text.style.left = '50%';
			text.style.top = '100%';
			text.style.transform = 'translate(-50%, -105%)';
			text.style.width = '75%';
			text.style.borderRadius = '5px';
			text.style.fontSize = '100%';
		}
		for ( let blurb of slideshowBlurbs ) {
			blurb.style.display = 'inline-block';
			blurb.style.opacity = '1';
		}
		
		for ( let textToggle of slideshowTextToggleArray ) {
			textToggle.style.display = 'none';
		}
	}
	else if ( window.innerWidth <= 768 ) {
		isActiveSlideshowOverlay = false;
		portfolioSlideshow.style.display = 'block';
		if  ( (window.innerHeight - header.offsetHeight) / window.innerWidth > 3/4 ) {
			portfolioSlideshow.style.top = 'calc(50% + var(--header-height-small)/2)';
			portfolioSlideshow.style.width = '100%';
			portfolioSlideshow.style.height = 'auto';
		}
		else {
			portfolioSlideshow.style.top = 'calc(50% + var(--header-height-small)/2)';
			portfolioSlideshow.style.height = window.innerHeight - header.offsetHeight + 'px';
			portfolioSlideshow.style.width = (4/3) * ( window.innerHeight - header.offsetHeight ) + 'px';
		}
		overlay.style.display = 'none';
		exitSlideshowButton.style.display = 'none';
		for ( let text of slideshowTexts ) {
			text.style.left = '0';
			text.style.width = 'auto';
			text.style.fontSize = '90%';
			text.style.borderRadius = '0';
			text.style.transform = 'translate(0%, -100%)';
			if ( text == slideshowTexts[currentImg] ) {
				text.style.opacity = '1';
			}
			else {
				text.style.opacity = '0';
			}
		}
		for ( let toggle of slideshowTextToggleArray ) {
			if ( toggle == slideshowTextToggleArray[currentImg] ) {
				toggle.style.opacity = '1';
			}
			else {
				toggle.style.opacity = '0';
			}
		}
		for ( let blurb of slideshowBlurbs ) {
			blurb.style.display = 'none';
		}
		for ( let img of slideshowImgs ) {
			if ( img == slideshowImgs[currentImg] ) {
				img.style.opacity = '1';
			}
			else {
				img.style.opacity = '0.4';
			}
		}
		for ( let textToggle of slideshowTextToggleArray ) {
			textToggle.style.display = 'flex';
		}
		for ( let backing of slideshowImgBackings ) {
    		backing.style.opacity = '1';
		}
		for ( let control of slideshowControls ) {
			control.style.opacity = '1';
		}
		if ( portfolioSlideshow.offsetTop - portfolioSlideshow.offsetHeight / 2 < portfolioTitle.offsetTop + portfolioTitle.offsetHeight && portfolioSlideshow.offsetWidth < window.innerWidth ) {
			portfolioTitle.style.visibility = 'hidden';
			// portfolioSlideshow.style.height = '85vh';
			// portfolioSlideshow.style.width = 'calc(4/3 * 85vh)';
			// portfolioSlideshow.style.top = header.offsetHeight / 2 + window.innerHeight / 2 + 'px';
			// portfolioSlideshow.style.transform = 'translate(-50%, -50%)';
		}
		else {
			portfolioTitle.style.visibility = 'visible';
			// portfolioSlideshow.style.height = 'auto';
			// portfolioSlideshow.style.width = '100%';
			// portfolioSlideshow.style.top = '55%';
		}
		if ( portfolioSlideshow.offsetTop + portfolioSlideshow.offsetHeight / 2 > portfolioNext.offsetTop - (portfolioNext.offsetHeight / 2) * 1.1 ) {
			portfolioNext.style.visibility = 'hidden';
		}
		else {
			portfolioNext.style.visibility = 'visible';
		}
	}
}


window.onload = function () {
	document.getElementById('intro').scrollIntoView();
	setTimeout( function () {
		navbarFormat();
		portfolioFormat();
		for ( let item of navItems ) {
			if ( window.pageYOffset >= header.offsetHeight ) {
				item.style.color = '#888';
			}
			else {
				item.style.color = '#191919';
			}
		}
	}, 125);
}
