import polka from "polka";
import { json as jsonBody } from "body-parser";
import { BotController, getBrowser } from "./bot";
import { Browser } from "puppeteer";

(async function() {
// Drop privileges

const server = polka();
let browser: Browser | null = null;

server.use(jsonBody());
/**
 * Requests the administrator visit a page or series of pages
 * Input:
 * {url: url}
 */
server.post('/visit', async (req, res) => {
    if(!req.body.url) {
        res.statusCode = 400;
        return res.end('No url specified');
    }

    if(typeof req.body.url === "string") {
        req.body.url = [req.body.url];
    }

    const controller = new BotController(browser!);
    await controller.init();
    controller.shield(+req.body.timeout || 10000);
    controller.enableDebug();

    try {
        for(const url of req.body.url) {
            console.log(`Visiting Requested [${url}]`);
            await controller.visit(url);
        }
    } catch(ex) {
        console.error('Error fetching page', ex)
        res.statusCode = 500;
        return res.end(JSON.stringify({
            detail: "Failed to fetch URL",
            exception: ex.toString()
        }));
    } finally {
        controller.close().catch(err => {
            console.error('Error during closing: ', err);
        });
    }

    return res.end('1');
});

server.listen(80, async (err: Error) => {
    if(err) throw err;
    process.setgid('xssbot');
    process.setuid('xssbot');
    browser = await getBrowser();

    console.log('XSSBot started and ready to accept requests');
});
})();