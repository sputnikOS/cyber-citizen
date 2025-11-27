// Creates the Sine Wave //
$(function(){
  var waves = new SineWaves({
    el: document.getElementById('waves'),
    speed: 1,
    width: function() {
      return $(window).width();
    },
    height: function() {
      return $(window).height();
    },
    wavesWidth: '95%',
    ease: 'SineInOut',
    waves: [
      {
        timeModifier: 1,
        lineWidth: 4,
        amplitude: 120,
        wavelength: 500,
        segmentLength: 1,
        type: 'Fibonacci'
      },
      {
        timeModifier: 1,
        lineWidth: 2,
        amplitude: -75,
        wavelength: 100,
        segmentLength: 1,
        type: 'Fibonacci'
      },
      {
        timeModifier: 1,
        lineWidth: 5,
        amplitude: -150,
        wavelength: 100,
        segmentLength: 1,
        type: 'Fibonacci'
      },
      {
        timeModifier: 2,
        lineWidth: 1,
        amplitude: 200,
        wavelength: 100,
        segmentLength: 1,
        type: 'Fibonacci'
      },
      {
        timeModifier: 2,
        lineWidth: 2,
        amplitude: -150,
        wavelength: 100,
        segmentLength: 1,
        type: 'Square'
      },
      {
        timeModifier: 2,
        lineWidth: 5,
        amplitude: -100,
        wavelength: 200,
        segmentLength: 1,
        type: 'Sine'
      }
    ],
    initialize: function (){
    },
    resizeEvent: function() {
      var gradient = this.ctx.createLinearGradient(0, 0, this.width, 0);
      gradient.addColorStop(0,"rgba(000, 000, 255, 0)");
      gradient.addColorStop(0.5,"rgba(0, 192, 255, 1)");
      gradient.addColorStop(1,"rgba(000, 000, 255, 0)");
      var index = -1;
      var length = this.waves.length;
        while(++index < length){
        this.waves[index].strokeStyle = gradient;
      }
      // Clean Up
      index = void 0;
      length = void 0;
      gradient = void 0;
    }
  });
});
