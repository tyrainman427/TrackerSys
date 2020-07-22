let myConfig = {
type: 'bar',
title: {
  text: 'Data Basics',
  fontSize: 24,
},
legend: {
  draggable: true,
},
scaleX: {
  // Set scale label
  label: { text: 'Techs' },
  // Convert text on scale indices
  labels: [ 'Admin', 'Etty', 'John' ]
},
scaleY: {
  // Scale label with unicode character
  label: { text: 'Tickets' }
},
plot: {
  // Animation docs here:
  // https://www.zingchart.com/docs/tutorials/styling/animation#effect
  animation: {
    effect: 'ANIMATION_EXPAND_BOTTOM',
    method: 'ANIMATION_STRONG_EASE_OUT',
    sequence: 'ANIMATION_BY_NODE',
    speed: 275,
  }
},
series: [
  {
    // plot 1 values, linear data
    values: [23,20,27],
    text: 'Low',
  },
  {
    // plot 2 values, linear data
    values: [35,42,33],
    text: 'Medium'
  },
  {
    // plot 2 values, linear data
    values: [15,22,13],
    text: 'High'
  }
]
};

zingchart.render({
    id: 'myChart',
    data: myConfig,
  });
