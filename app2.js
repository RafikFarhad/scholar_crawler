var request = require("request");
var cheerio = require("cheerio");
var fs = require("fs");
var changeCase = require('change-case')
var util = require('util')


var baseUrl = "https://scholar.google.com";

publications = getUser().then((result) => {
  newLine(' END ');
  // console.log('@@@', result.get());
  a = result.get()
  try {
    a[0].then((result) => {
      console.log(result)
    })
  }
  catch(e) {
    console.log('====', e);
  }
});

async function getUser() {
  var url = baseUrl + "/citations?user=6F3Kj_8AAAAJ";
  var data = '';
  data = fs.readFileSync('test.txt', 'utf8');
  var $ = cheerio.load(data)

  var publications = await $('form div table tbody tr').map(async function (index, element) {
    if(index > 0) return;
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
      .then( () => {
        newLine('#');
        console.log(publication)
      })
  })
  console.log(JSON.stringify('->', publications.get(), null, 2))
  return publications;
}

async function getDetailsInfo(publication) {
  console.log('Details Fetching...');
  const req = util.promisify(request)
  await request(baseUrl + publication.href, function(err, resp, body) {
    if (err) {
      throw err;
    }
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
    })
    return publication;
}

function newLine(c = "-") {
  console.log(c.repeat(78));
}
function getValue(data) {
  return data ? data : null;
}