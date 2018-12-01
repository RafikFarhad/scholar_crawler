var request = require("request");
var cheerio = require("cheerio");
var fs = require("fs");
var changeCase = require('change-case')
var util = require('util')
const r2 = require("r2");
var async = require("async");
require('dotenv').config();


var baseUrl = "https://scholar.google.com";

getUser("6F3Kj_8AAAAJ");

async function getUser(user_id) {
  var url = baseUrl + "/citations?user=" + user_id;
  var data = '';
  data = fs.readFileSync('test.txt', 'utf8');
  data = await r2(url).text
  console.log(data);
  var $ = cheerio.load(data);
  var result = [];
  var publications = $('form div table tbody tr');

  async.forEachOf(publications, async (value, index, callback) => {
    if(index > 0) return;
    element = value;
    var publication = {};
    trs = $(element)
    trs.children('td').map((index, element2) => {
      if(index == 0) {
        td = $(element2.children[0])
        publication.title = td.text();
        publication.href = td.data('href');
        td = $(element2.children[1])
        td = $(element2.children[2])
        publication.publisher = td.text()

      }
      else if(index == 1){
        td = $(element2.children[0])
        publication.citation = td.text()?td.text():0;
      } else if(index == 2){
        td = $(element2.children[0])
        publication.publish_date = td.text()?td.text():0;
      }
    })
    // console.log(JSON.stringify(publication, null, 4));
    newLine('*');
    publication = await getDetailsInfo(publication)
      .then( (_) => {
        newLine('#');
        // console.log(publication)
        // console.log(result)
        result.push(publication);
        return publication;
      })
      result.push(publication);
      console.log(publication)
}, err => {
    if (err) console.error(err.message);
});

  // for(index = 0; index<publications.length; index++) {
  //   if(index > 1) return;
  //   element = publications[index]
  //   var publication = {};
  //   trs = $(element)
  //   trs.children('td').map((index, element2) => {
  //     if(index == 0) {
  //       td = $(element2.children[0])
  //       publication.title = td.text();
  //       publication.href = td.data('href');
  //       td = $(element2.children[1])
  //       td = $(element2.children[2])
  //       publication.publisher = td.text()

  //     }
  //     else if(index == 1){
  //       td = $(element2.children[0])
  //       publication.citation = td.text()?td.text():0;
  //     } else if(index == 2){
  //       td = $(element2.children[0])
  //       publication.publish_date = td.text()?td.text():0;
  //     }
  //   })
  //   // console.log(JSON.stringify(publication, null, 4));
  //   newLine('*');
  //   publication = await getDetailsInfo(publication)
  //     .then( (_) => {
  //       newLine('#');
  //       // console.log(publication)
  //       // console.log(result)
  //       result.push(publication);
  //       return publication;
  //     })
  //     result.push(publication);
  //     console.log(publication)
  // }
  // console.log(JSON.stringify('->', publications.get(), null, 2))
  // .map(async function (index, element) {
  // }) 
  // publications = result; 
  // console.log(result);
  return result;
}

async function getDetailsInfo(publication) {
  console.log('Details Fetching...');
  // await request(baseUrl + publication.href, function(err, resp, body) {
    body = await r2(baseUrl + publication.href).text
    // body = fs.readFileSync('test2.txt', 'utf8');
    // console.log(body);
    var $ = cheerio.load(body);
    var forms = $("form");
    //console.log(infos);
    var infos = $(forms[0])
      .children("div")
      .map((index, element) => {
        div = $(element);
        if (index == 0) {
          pdf_link = div.find("div div a");
          publisher_link = div.find("#gsc_vcd_title a");
          publication.publisher_link = getValue(publisher_link.attr("href"));
          publication.pdf_link = getValue(pdf_link.attr("href"));
        } else {
          div.children('div').map((index, element) => {
            if(index>5) {
              return;
            }
            var tableDiv = $(element);
            var Index = $(element.children[0]);
            var data = $(element.children[1]);
            if(Index.text()) {
              publication[changeCase.snakeCase(Index.text())] = getValue(data.text());
            }
          });
          // console.log(div.text());
        }
        // newLine();
      });
      // console.log(JSON.stringify(publication, null, 2));
    // })
    try {
      request.post({url:process.env.PUSH_API, formData: publication},
        function optionalCallback(err, httpResponse, body) {
        if (err) {
          return console.error('failed:', err.code);
        }
        console.log('Successful!  Server responded with:', body);
      });
    } catch(e) {
      // console.error(e);
    }
    return publication;
}

function newLine(c = "-") {
  console.log(c.repeat(78));
}
function getValue(data) {
  return data ? data : null;
}