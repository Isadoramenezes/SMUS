const gauge = c3.generate({
  bindto: '#gauge',
  data  : {
    columns: [
      ['umidade', 0]
    ],
    type   : 'gauge',
  },
  gauge : {
    label: {
      format: (value, ratio) => {
        return value + ' %';
      },
      show  : false
    },
    min  : 0,
    max  : 50,
    units: ' %',
  },
  color : {
    pattern  : ['#227EAF', '#F97600'],
    threshold: {
      unit  : '%',
      max   : 50,
      values: [10, 30]
    }
  },
  size  : {
    height: 180
  }
});

const getValueGauge = () => { return gauge.data.values('umidade')[0] };

const setGaugeValue = (value) => {
  gauge.load({
    columns: [
      ['umidade', value]
    ]
  });
};