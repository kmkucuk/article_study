import express from "express";
import { engine } from 'express-handlebars';
import * as fs from "node:fs"
import { parse } from 'csv-parse/sync';

const app = express();

// Static Files
app.use(express.static(`./public`));

// Templating
app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', './html');


const fontCSS = `
`;
const regex = new RegExp(/\[(.*?)\]/g)
/**
 * 
 * @param {string} text 
 * @param {boolean} convertLinksToAnchors 
 * @returns string
 */
function parseLinks(text, convertLinksToAnchors) {
        let parts;
        let output = text;
    do {
        parts = regex.exec(text)
        if (!parts) {
            return output
        }
        if (convertLinksToAnchors) {
            output = output.replace(parts[0], `<a href="https://google.com">${parts[1]}</a>`)
        }
        else {
            output = output.replace(parts[0], parts[1])

        }
    } while (parts != null)

}

//Routes
app.get('/', (req, res) => {
    const queryParams = new URLSearchParams(req.query);

    const article = queryParams.get('article');
    const useLinks = queryParams.get('links').toLowerCase() === "true";
    let font = queryParams.get('font').replace(/\W/g, "_").toLowerCase();
    
    if (!font) {
        return res.status(400).send("<h1>Font cannot be null</h1>")

    }

    const parsed = parse(fs.readFileSync(`../articles/article${article}/article_sheet.csv`))
    const headers = []

    const input = {
        body: [],
        css: font
    }

    for (let line of parsed) {
        let [type, color, style, weight, content] = line
        if (type === 'type') {
            continue
        }

        switch (type) {
            case "header":
                headers.push(content)
                break;
            case "text":
                input.body.push(parseLinks(content, useLinks))
                break;
            case "author":
                input[type] = content.replace("By: ", "");
                break;
            default:
                input[type] = content
        }


    }

    input["title"] = headers[0]
    input["subtitle"] = headers[1]
    
    res.render("index", input)
})

app.listen(8090, (output) => {

    console.log(output)
    console.log("listening on http://localhost:8090")
})
