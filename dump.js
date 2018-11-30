
// var connection = mysql.createConnection({
//   host: 'localhost',
//   user: '',
//   password: '',
//   database: ''
// })
// connection.connect()


// var count = 1
// request('http://scholar.google.com/citations?view_op=view_citation&hl=en&oe=ASCII&user=6F3Kj_8AAAAJ&citation_for_view=6F3Kj_8AAAAJ:_FxGoFyzp5QC', function(err, resp, body) {
//   if (err) throw err
//   console.log(body)
//   var $ = cheerio.load(body)
//   var publications = $('form div table tbody tr').each( function (index, element) {
//     tr = cheerio.load(element)
//     tds = tr('td').each((index,td) => {
//       td = cheerio.load(td)
//       // console.log(td.html())
//     });
//   })
//   console.log(body);

// })

// var data = "";
// data = fs.readFileSync("test2.txt", "utf8");
// // data = fs.readFileSync('test3.txt', 'utf8');
// var publication = {};


// var infos = $('form div').map((index, element) => {
//   // if(index > 1) return;
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
//   console.log(JSON.stringify(publication, null, 4));
//   newLine();
//   return publication;
// })