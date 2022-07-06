function makeThumb(page) {
    // draw page to fit into 96x96 canvas
    var vp = page.getViewport(1);
    var canvas = document.createElement("canvas");
    canvas.width = canvas.height = 96;
    var scale = Math.min(canvas.width / vp.width, canvas.height / vp.height);
    return page.render({canvasContext: canvas.getContext("2d"), viewport: page.getViewport(scale)}).promise.then(function () {
      return canvas;
    });
  }
  
  pdfjsLib.getDocument("https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/compressed.tracemonkey-pldi-09.pdf").promise.then(function (doc) {
    var pages = []; while (pages.length < doc.numPages) pages.push(pages.length + 1);
    return Promise.all(pages.map(function (num) {
      // create a div for each page and build a small canvas for it
      var div = document.createElement("div");
      document.body.appendChild(div);
      return doc.getPage(num).then(makeThumb)
        .then(function (canvas) {
          div.appendChild(canvas);
      });
    }));
  }).catch(console.error);