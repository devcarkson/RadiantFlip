(function() {
  'use strict';

  //menu fix mobile

  let vh = window.innerHeight * 0.01;
  // Then we set the value in the --vh custom property to the root of the document
  document.documentElement.style.setProperty('--vh', `${vh}px`);

  window.addEventListener('resize', () => {
    // We execute the same script as before
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });
  


  svg4everybody();
  

  //table
  
  if($('table.responsive').length > 0){
    $('table.responsive').ngResponsiveTables();
  }
	
  //select styler

  //datepicker

  // $( ".datepicker" ).datepicker();

  // $("#weeklyDatePicker").datetimepicker({
  //   format: 'DD-MM-YYYY'
  // });

  // //Get the value of Start and End of Week
  // $('#weeklyDatePicker').on('dp.change', function (e) {
  //     var value = $("#weeklyDatePicker").val();
  //     var firstDate = moment(value, "DD-MM-YYYY").day(0).format("DD-MM-YYYY");
  //     var lastDate =  moment(value, "DD-MM-YYYY").day(6).format("DD-MM-YYYY");
  //     $("#weeklyDatePicker").val(firstDate + " - " + lastDate);
  // });
   
  //tabs

  $('.tabs__wrap').each(function() {
    $(this).find('.tab').each(function(i) {
      $(this).parents('.tabs__wrap').find('.tab_content').children().not(':first').hide();
      $(this).click(function(){
        $(this).addClass('active').siblings().removeClass('active')
        $(this).parents('.tabs__wrap').find('.tab_content').children().eq(i).fadeIn(0).siblings('.tab_item').hide();
      
        // $(".nicescroll-box").getNiceScroll().resize();
      });
    });
  });

  //tabs
  $('[data-tabs-btn]').click(function() {
    let tabsName = $(this).parent().attr('data-tabs-btns');
    let tabNo = $(this).attr('data-tabs-btn');
    let tabsWrapper = $('[data-tabs-wrapper='+tabsName+']');

    $(this).siblings().removeClass('active');
    $(this).addClass('active');

    tabsWrapper.children().each(function(i, item) {
      $(item).hide();
      if ($(item).attr('data-tabs-item') === tabNo) {
        $(item).show().addClass('active').siblings().removeClass('active');
      }
    });
  });

  function tabsInitialization() {
    let btns = $('[data-tabs-btns]');
    let wrapper = $('[data-tabs-wrapper]');

    $(wrapper).children().not(function() {
      if ($(this).attr('data-tabs-item') === '1') {
        return true;
      }
    }).hide();

    $(btns).children().not(function() {
      if ($(this).attr('data-tabs-btn') === '1') {
        return false;
      } else {
        return true;
      }
    }).addClass('active');
  }
  
  tabsInitialization();

  //accordion

  var Accordion = function(el, multiple) {
    this.el = el || {};
    this.multiple = multiple || false;

    // Variables privadas
    var links = this.el.find('.accordion__head');
    // Evento
    links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
  }

  Accordion.prototype.dropdown = function(e) {
    var $el = e.data.el,
        $this = $(this),
        $next = $this.next();

    $next.slideToggle();
    $this.parent().toggleClass('active');

    if($('.nicescroll-box').length !== 0){
      setTimeout(() => {
        $(".nicescroll-box").getNiceScroll().resize();
      }, 1000);
    }

    if (!e.data.multiple) {
      $el.find('.accordion__body').not($next).slideUp().parent().removeClass('active');
    };
  }	

  var accordion = new Accordion($('.accordion'), false);
  
  //nicescroll

  $(".nicescroll-box").niceScroll(".wrap",{
    cursorcolor:"#F67942",
    cursorwidth:"2px",
    cursorborder: "0px solid #fff",
    zindex: 20,
    emulatetouch: true,
    autohidemode: false,
    cursorborderradius: "0px",
    railalign: 'right',
  });
  
  
  // aos

	
	//clipboard

  var affil1 = new Clipboard('.copy-text');

  function affiliatelink(id) {
    id.on('success', function (e) {

      $('.copy-success').fadeIn();
      $('.copy-success').delay(3000).fadeOut();
    });
  }

  affiliatelink(affil1);

  $('.header-burger').on('click', function(){
    $(this).toggleClass('active');
    $('.header-side').toggleClass('active');
  })
  $('.cab-burger').on('click', function(){
    $(this).toggleClass('active');
    $('.cab-menu').toggleClass('active');
  })

  $('.invest-nav__arrow.prev').on('click', function(){
    if($('.invest-tabs__item.active').prev().length == 0){
      $('.invest-tabs__item').last().addClass('active').siblings().removeClass('active');
    }else{
      $('.invest-tabs__item.active').removeClass('active').prev().addClass('active');
    }
    
    if($('.invest-plan__list.active').prev().length == 0){
      $('.invest-plan__list').last().show().addClass('active').siblings().hide().removeClass('active');
    }else{
      $('.invest-plan__list.active').hide().removeClass('active').prev().show().addClass('active');
    }
  })

  $('.invest-nav__arrow.next').on('click', function(){
    if($('.invest-tabs__item.active').next().length == 0){
      $('.invest-tabs__item').first().addClass('active').siblings().removeClass('active');
    }else{
      $('.invest-tabs__item.active').removeClass('active').next().addClass('active');
    }
    
    if($('.invest-plan__list.active').next().length == 0){
      $('.invest-plan__list').first().show().addClass('active').siblings().hide().removeClass('active');
    }else{
      $('.invest-plan__list.active').hide().removeClass('active').next().show().addClass('active');
    }
  })

  // sliders

  var teamHeroSlider = new Swiper('.team-hero .swiper', {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 0,
    centeredSlides: true,
    effect: 'fade',
    fadeEffect: {
      crossFade: true
    },
    autoplay: {
      delay: 3000,
      disableOnInteraction: true,
    },
    navigation: {
      nextEl: '.team-nav .swiper-button-next',
      prevEl: '.team-nav .swiper-button-prev',
    },
  });


  var footerWalletsSlider = new Swiper('.footer-wallets .swiper', {
    loop: true,
    slidesPerView: 2,
    spaceBetween: 0,
    // centeredSlides: true,
    // effect: 'fade',
    // fadeEffect: {
    //   crossFade: true
    // },
    autoplay: {
      delay: 3000,
      disableOnInteraction: true,
    },
    navigation: {
      nextEl: '.footer-wallets .swiper-button-next',
      prevEl: '.footer-wallets .swiper-button-prev',
    },
    breakpoints: {
      1200: {
        slidesPerView: 6,
      },
      768: {
        slidesPerView: 4,
      }
    }
  });

  
})();