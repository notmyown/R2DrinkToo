function BarBot(container) {
  var barBot;
  var serverurl;

  var docW = 0;
  var docH = 0;
  var ratio = 1;

  var spanimg = '';

  this.state = {
  }

  this.getWindowSize = function getWindowSize() {
    docH = $("body").height();
    docW = $("body").width();
    if (docW > 480) {
      docW = 480;
    } else { }
    if (docH > 320) {
      docH = 320;

    }
    $(".barbot_size").height(docH);
    $(".barbot_size").width(docW);
    ratio = 1;//Math.round(docW/2) / 230;
  }

  this.generate = function generate() {
    this.serverurl = window.localStorage.getItem("barbot_server");
    if (!this.serverurl || this.serverurl.length < 1) {
      this.serverurl = "http://localhost:5000/barbot";
    }
    this.spanimg = '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">';
    if (!container) {
      container = "body";
    }
    var
      output = "<div class='r2d2'>";
    output += "<div class='headline' style='height: 10vh;'>";
    output += "<div class='interface'>";
    output += "<div class='interfacetop'>";
    output += "<div class='ithead'></div>";
    output += "<div class='itheado'></div>";
    output += "<div class='itheadeye'></div>";
    output += "</div>";
    output += "<div class='interfacebottom'>";
    output += "<div class='ib1'></div>";
    output += "<div class='ib2'></div>";
    output += "<div class='ib3'><div></div><div></div></div>";
    output += "<div class='ib4'></div>";
    output += "<div class='ib5'>";
    output += "<div class='blackhalf'>";
    output += "<img class='bhleft' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
    output += "<img class='bhcenter' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
    output += "<img class='bhright' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
    output += "</div>";
    output += "<div class='redcircle'><img class='red' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'></div>";
    output += "</div>";
    output += "<div class='ib6 menu'><img class='ratio' src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'><div></div><div></div><div></div></div>";
    output += "</div>";
    output += "</div>";
    output += "</div>";
    output += "<div class='barbot_size'>";
    output += "<div class='barbot_loadingpage'>";
    output += "<div class='barbot_loadingpage_star'>";
    output += "<img class='introbg' src='/static/img/R2D2Dance.gif'/>";
    output += "<br>Loading..."
    output += "</div>";
    output += "</div>";
    output += "<div class='barbot_orderpage'>";
    output += "<div class='barbot_orderpage_content'>";
    output += "</div>";
    output += "</div>";
    output += "<div class='barbot_settingspage'>";
    output += "<div class='barbot_settingspage_content'>";
    output += "</div>";
    output += "</div>";
    output += "</div>";
    output += "</div>";

    $(container).html(output).addClass("barbot");
    $(".r2d2 .headline .menu").click(function () {
      barBot.click.menu();
    });
  }

  this.init = function init() {
    //this.getWindowSize();
    barBot = this;

    window.setTimeout(function () {
      barBot.resize();
      barBot.communication.init();
    }, 500);

    $(window).on("orientationchange", function () {
      barBot.resize();
    });
    $(window).resize(function () {
      barBot.resize();
    });
  }

  this.resize = function resize() {
    //this.getWindowSize();
    if (docH < docW) {
      $("body").addClass("quer").removeClass("hoch");

    } else {
      $("body").removeClass("quer").addClass("hoch");
    }
  }

  this.click = {
    menu: function menuClick() {
      $(".barbot .barbot_loadingpage").hide();
      $(".barbot .barbot_orderpage").hide();
      $(".barbot .barbot_settingspage").show();
      $(".barbot .barbot_settingspage .barbot_settingspage_content").html("");
      var output = "";
      output += "<div class='menubutton' id='addcocktail'>cocktail hinzufügen</div>";
      output += "<div class='menubutton' id='addingredients'>zutaten verwalten</div>";
      output += "<div class='menubutton' id='configureslots'>r2drinktoo befüllen</div>";
      output += "<div class='menubutton' id='back'>zurück</div>";
      $(".barbot .barbot_settingspage .barbot_settingspage_content").html(output);
      $(".barbot .barbot_settingspage .barbot_settingspage_content #addcocktail").click(function () {
        barBot.click.addCocktail();
      });
      $(".barbot .barbot_settingspage .barbot_settingspage_content #addingredients").click(function () {
        barBot.click.addIngredients();
      });
      $(".barbot .barbot_settingspage .barbot_settingspage_content #configureslots").click(function () {
        barBot.click.configureSlots();
      });
      $(".barbot .barbot_settingspage .barbot_settingspage_content #back").click(function () {
        $(".barbot .barbot_loadingpage").hide();
        $(".barbot .barbot_orderpage").show();
        $(".barbot .barbot_settingspage").hide();
      });
    },

    addCocktail: function addCocktail() {
      $(".barbot .barbot_loadingpage").hide();
      $(".barbot .barbot_orderpage").hide();
      $(".barbot .barbot_settingspage").show();
      $(".barbot .barbot_settingspage .barbot_settingspage_content").html("<div class='flowcontainer'></div>");
      var output = "";
      output += "<div class='flowitem' id='plus'><img src='/static/img/plus.jpg'><div></div></div>";
      $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer").html(output);
      barBot.communication.loadCocktails("settingspage");
      $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer #plus").click(function () {
        var output = "";
        output += "<div>Cocktail hinzufügen<br>";
        output += "<label for='name'>Name</label>";
        output += "<input type='text' name='name' id='name' value=''><br>";
        output += "<label for='image'>Bild</label>";
        output += "<input type='file' name='image' id='image' value=''><br>";
        output += "<span>Zutaten:</span><br>";
        output += "<div class='addingredientscontainer'>";
        output += "<div class='flowingredient' id='addingredient'><img width='30' src='/static/img/plus.jpg'> Hinzufügen</div>"
        output += "</div>";
        output += "<input type='submit' value='Submit' id='submit'>";
        output += "</div>";
        $(".barbot .barbot_settingspage .barbot_settingspage_content").html(output);
        $(".barbot .barbot_settingspage .barbot_settingspage_content #submit").click(function () {
          barBot.communication.addCocktail();
        });
        $(".barbot .barbot_settingspage .barbot_settingspage_content #addingredient").click(function () {
          barBot.communication.addCocktailIngredient();
        });
      });
    },

    addIngredients: function addIngredients() {
      $(".barbot .barbot_loadingpage").hide();
      $(".barbot .barbot_orderpage").hide();
      $(".barbot .barbot_settingspage").show();
      $(".barbot .barbot_settingspage .barbot_settingspage_content").html("<div class='flowcontainer'></div>");
      var output = "";
      output += "<div class='flowitem' id='plus'><img src='/static/img/plus.jpg'><div></div></div>";
      $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer").html(output);
      barBot.communication.loadIngredients();
      $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer #plus").click(function () {
        var output = "";
        output += "<div>";
        output += "<label for='name'>Name</label>";
        output += "<input type='text' name='name' id='name' value=''><br>";
        output += "<label for='image'>Bild</label>";
        output += "<input type='file' name='image' id='image' value=''><br>";
        output += "<input type='submit' value='Submit' id='submit'>";
        output += "</div>";
        $(".barbot .barbot_settingspage .barbot_settingspage_content").html(output);
        $(".barbot .barbot_settingspage .barbot_settingspage_content #submit").click(function () {
          barBot.communication.addIngredient();
        });
      });
    },

    configureSlots: function configureSlots() {
      $(".barbot .barbot_loadingpage").hide();
      $(".barbot .barbot_orderpage").hide();
      $(".barbot .barbot_settingspage").show();
      $(".barbot .barbot_settingspage .barbot_settingspage_content").html("<div class='flowcontainer'></div>");
      var output = "";
      for (var i = 1; i < 9; i++) {
        output += "<div class='flowitem slot' id='slot" + i + "'><img src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'><div class='cocktail'><img src='/static/img/res/ingredients/empty.png'><div><div class='id'>" + i + "</div><div class='name red'>leer</div></div></div></div>";
      }
      $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer").html(output);
      barBot.communication.loadSlots("settingspage");
    }

  }

  this.communication = {
    init: function cominit() {
      window.setTimeout(function () {
        barBot.communication.stateinterval = window.setInterval(function () {
          $.ajax({ url: barBot.serverurl + "/status", dataType: 'jsonp', timeout: 1000, jsonp: "callback" })
            .done(function (data) {
              barBot.communication.loadCocktails();
              $(".barbot .barbot_loadingpage").hide();
              $(".barbot .barbot_orderpage").show();
              $(".barbot .barbot_settingspage").hide();
              barBot.resize();
              window.clearInterval(barBot.communication.stateinterval);
              barBot.communication.state();
              barBot.communication.stateinterval = window.setInterval(function () { barBot.communication.state() }, 1000);
              barBot.communication.timeoutcounter = 0;
              barBot.communication.loadCocktails("orderpage");
            })
            .always(function () {
              barBot.log("init interval");
            })
            .fail(function (data) {
              barBot.communication.connectionfailed();
              $(".barbot .barbot_loadingpage").hide();
              $(".barbot .barbot_orderpage").show();
              $(".barbot .barbot_settingspage").hide();
            });
        }, 1000);
      }, 1000);
    },
    timeoutcounter: 0,
    busyoverlay: 0,
    state: function comstate() {
      $.ajax({ url: barBot.serverurl + "/status", dataType: 'jsonp', timeout: 1000, jsonp: "callback" })
        .done(function (data) {
          barBot.state = data;
          barBot.communication.timeoutcounter = 0;
        })
        .always(function () {
          //console.log("state interval");
        })
        .fail(function (data) {
          barBot.communication.connectionfailed();
        });

    },
    connectionfailed: function comconnectionfailed() {
      barBot.communication.timeoutcounter++;
      console.log(barBot.communication.timeoutcounter);
      if (barBot.communication.timeoutcounter > 5) {
        window.clearInterval(barBot.communication.stateinterval);
        if (barBot.communication.timeoutcounter < 10) {
          $('<div></div>').appendTo('body')
            .html('<div><h6>Es konnte keine Verbindung zu R2DrinkToo hergestellt werden.</h6></div>')
            .dialog({
              modal: true,
              title: 'Verbindung unterbrochen',
              zIndex: 10000,
              autoOpen: true,
              width: '95%',
              resizable: false,
              buttons: {
                Einstellungen: function () {
                  barBot.communication.timeoutcounter = 0;
                  $(".barbot .barbot_loadingpage").hide();
                  $(".barbot .barbot_orderpage").hide();
                  $(".barbot .barbot_settingspage").show();
                  $(this).dialog("close");
                },
                Neustart: function () {
                  window.location.reload();
                }
              },
              close: function () {
                barBot.communication.timeoutcounter = 0;
                $(this).dialog("close");
                $(this).remove();
              }
            });
        }
        barBot.communication.timeoutcounter = 10;
      }
    },
    order: function comorder(num) {
      var reqdata = {
        drinkid: num
      }
      $.ajax({ url: barBot.serverurl + "/order", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          $(".barbot .barbot_orderpage .barbot_orderpage_content").html("<div class='cocktaildetail'></div>");
            var output = "";
            output += "<div class='name'><h1>" + data.name + "</h1></div>";
            output += "<div class='row'>";
            output += "<div class='ingredients'>Bitte stellen Sie ein Glas mit folgendem Inhalt in den Ausgabeschacht des R2DrinkToo<br><ul>";
            data.provided.forEach(function(s,i,o) {
                output += "<li>" + s + "</li>";
            });
            output += "</ul></div>";
            output += "<div class='ingredients'>Die folgenden Zutaten sind nicht im R2DrinkToo vorhanden. Wenn Sie fortfahren, müssen Sie die Inhaltsstoffe selbstständig ergänzen.<br><ul>";
            data.missing.forEach(function(s,i,o) {
                output += "<li>" + s + "</li>";
            });
            output += "</ul></div>";
            output += "<div class='id'>" + reqdata.drinkid + "</div>";
            output += "<div class='order'><div class='button'>fortfahren</div></div>";
            output += "</div>";
            output += "<div class='back'>Zurück</div>";
            $(".barbot .barbot_orderpage .barbot_orderpage_content .cocktaildetail").append(output);
            $(".barbot .barbot_orderpage .barbot_orderpage_content .cocktaildetail .back").click(function(){
                $(".barbot .barbot_loadingpage").hide();
                $(".barbot .barbot_orderpage").show();
                $(".barbot .barbot_settingspage").hide();
                barBot.communication.loadCocktails("orderpage");
            });
            $(".barbot .barbot_orderpage .barbot_orderpage_content .cocktaildetail .order .button").click(function(){
                barBot.communication.pumping(data.drinkid);
            });
        });
    },
    pumping: function compump(num) {
      var reqdata = {
        drinkid: num
      }
      $.ajax({ url: barBot.serverurl + "/pumping", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          $(".barbot .barbot_orderpage .barbot_orderpage_content").html("<div class='cocktaildetail'></div>");
            var output = "";
            output += "<div class='name'><h1>" + data.name + "</h1></div>";
            output += "<div class='row'>";
            output += "Bitte Warten"
            output += "<div class='id'>" + reqdata.drinkid + "</div>";
            output += "<div class='order'><div class='button'></div></div>";
            output += "</div>";
            output += "<div class='back'>Zurück</div>";
            $(".barbot .barbot_orderpage .barbot_orderpage_content .cocktaildetail").append(output);
            $(".barbot .barbot_orderpage .barbot_orderpage_content .cocktaildetail .back").click(function(){
                $(".barbot .barbot_loadingpage").hide();
                $(".barbot .barbot_orderpage").show();
                $(".barbot .barbot_settingspage").hide();
                barBot.communication.loadCocktails("orderpage");
            });
        });
    },
    loadCocktails: function loadCocktails(page) {
      var reqdata = {
      }
      $.ajax({ url: barBot.serverurl + "/list_drinks", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          if (data && data.list) {
            var output = "";
            var flowcontainer = $(".barbot .barbot_" + page + " .barbot_" + page + "_content .flowcontainer")[0];
            if (!flowcontainer) {
              $(".barbot .barbot_" + page + " .barbot_" + page + "_content").html("<div class='flowcontainer'></div>");
            }
            data.list.forEach(function (s, i, o) {
              output += "<div class='flowitem'><img src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
              output += "<div class='cocktail'>";
              output += "<img src='/static/img/res/cocktails/" + s.image + "'>";
              output += "<div class='name'>" + s.name + "</div>";
              output += "<div class='id'>" + s.id + "</div>";
              output += "</div>";
              output += "</div>";
            });
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content .flowcontainer").append(output);
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content .flowcontainer .cocktail").click(function() {
              var id = $(this).find(".id").text();
              barBot.communication.loadCocktail(page, id);
            });
          }
        });
    },
    loadCocktail: function loadCocktail(page, id) {
      var reqdata = {
        drinkid: id
      }
      $.ajax({ url: barBot.serverurl + "/drink_info", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          if (data && data.name) {
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content").html("<div class='cocktaildetail'></div>");
            var output = "";
            output += "<div class='name'><h1>" + data.name + "</h1></div>";
            output += "<div class='row'>";
            output += "<div class='image'><img src='/static/img/res/cocktails/" + data.image + "'></div>";
            output += "<div class='ingredients'><ul>";
            data.ingredients.forEach(function(s,i,o) {
                output += "<li>" + s.ingredient;
                if (s.provided) {
                output += " (" + s.amount + ")";
                }
                output += "</li>";
            });
            output += "</ul></div>";
            output += "<div class='order'><div class='button'>bestellen</div></div>";
            output += "</div>";
            output += "<div class='id'>" + data.drinkid + "</div>";
            output += "<div class='back'>Zurück</div>";
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content .cocktaildetail").append(output);
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content .cocktaildetail .back").click(function(){
                $(".barbot .barbot_loadingpage").hide();
                $(".barbot .barbot_orderpage").show();
                $(".barbot .barbot_settingspage").hide();
                barBot.communication.loadCocktails("orderpage");
            });
            $(".barbot .barbot_" + page + " .barbot_" + page + "_content .cocktaildetail .order .button").click(function(){
                barBot.communication.order(data.drinkid);
            });
          }
        });
    },
    loadIngredients: function loadIngredients() {
      var reqdata = {
      }
      $.ajax({ url: barBot.serverurl + "/list_ingredients", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          if (data && data.list) {
            var output = "";
            data.list.forEach(function (s, i, o) {
              output += "<div class='flowitem'><img src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
              output += "<div class='cocktail'>";
              output += "<img src='/static/img/res/ingredients/" + s.image + "'>";
              output += "<div class='name'>" + s.name + "</div>";
              output += "<div class='id'>" + s.id + "</div>";
              output += "</div>";
              output += "</div>";
            });
            $(".barbot .barbot_settingspage .barbot_settingspage_content .flowcontainer").append(output);
          }
        });
    },
    addIngredient: function addIngredient() {
      var reqdata = {
        name: $(".barbot .barbot_settingspage .barbot_settingspage_content #name").val(),
        image: $(".barbot .barbot_settingspage .barbot_settingspage_content #image").val()
      }
      $.ajax({ url: barBot.serverurl + "/add_ingredient", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          barBot.click.addIngredients();
        });
    },
    addCocktail: function addCocktail() {
      var ing = "";
      $(".barbot .barbot_settingspage .barbot_settingspage_content .addingredientscontainer .flowingredient.new").each(function(s,i,o){
        var aning = $(this).find("select").val() + "_";
        aning += $(this).find(".amount").val() + "_";
        aning += $(this).find(".provided").val();
        ing += aning + "-";
      });
      var reqdata = {
        name: $(".barbot .barbot_settingspage .barbot_settingspage_content #name").val(),
        image: $(".barbot .barbot_settingspage .barbot_settingspage_content #image").val(),
        ingredients: ing
      }
      $.ajax({ url: barBot.serverurl + "/add_cocktail", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          barBot.click.addCocktail();
        });
    },
    addCocktailIngredient: function addCocktailIngredient() {
      var reqdata = {
      }
      $.ajax({ url: barBot.serverurl + "/list_ingredients", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          if (data && data.list) {
            var output = "";
            output += "<div class='flowingredient new'><img width='30' src='/static/img/minus.jpg' class='removeingredient'><div><select>";
            data.list.forEach(function (s, i, o) {
              output += "<option value='" +  s.id + "'>" + s.name + "</option>";
            });
            output += "</select></div><div>Menge:<input class='amount' value='0'/></div><div>Vorrausgesetz: <input type='checkbox' class='provided'/><div></div></div>";
            $(".barbot .barbot_settingspage .barbot_settingspage_content .addingredientscontainer").append(output);
            $(".barbot .barbot_settingspage .barbot_settingspage_content .addingredientscontainer img:last").click(function(e) {
              $(e.target.parentNode).remove();
            });
          }
        });
    },
    loadSlots: function loadSlots() {
      var reqdata = {
      }
      $.ajax({ url: barBot.serverurl + "/list_slots", dataType: 'jsonp', jsonp: "callback", data: reqdata })
        .always(function (data) {
          if (data && data.list) {
            var output = "";
            data.list.forEach(function (s, i, o) {
                output = "<img src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'>";
                output += "<div class='cocktail'>";
              if (!s.name || s.name == "None") {
                output += "<img src='/static/img/res/ingredients/empty.png'>";
              } else {
                output += "<img src='/static/img/res/ingredients/" + s.image + "'>";
                output += "<div class='name'>" + s.name + "</div>";
                output += "<div class='ingredient'>" + s.ingredient + "</div>";
              }
              output += "<div class='id'>" + s.id + "</div>";
              output += "</div>";
              $("#slot" + s.id).html(output).addClass("slot");
            });
          }
        });
    }
  }

  this.log = function log(text) {
    $("#log").html(text);
  }
  
  //init
  this.generate();
};
