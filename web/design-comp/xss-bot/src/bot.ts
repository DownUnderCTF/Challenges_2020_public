import puppeteer from "puppeteer";
import { URLValidator } from "./sec";

type RequestInterceptor = (e: puppeteer.Request, ...args: any) => boolean;

export class BotController {
    readonly #browser: puppeteer.Browser;
    #context: puppeteer.BrowserContext | null = null;
    #page: puppeteer.Page | null = null;
    #requestInterceptors: RequestInterceptor[] = [];
    #timeout: NodeJS.Timeout | null = null;

    constructor(readonly browser: puppeteer.Browser) {
        this.#browser = browser;
        this.#requestInterceptors = []
    }

    public async init() {
        this.#context = await this.#browser.createIncognitoBrowserContext();
        this.#page = await this.#context.newPage();
        await this.#page.setRequestInterception(true);
        this.#page!.on('request', request => {
            if(this.#requestInterceptors.every(handler => handler(request))) {
                request.continue();
            }
        });
    }

    public async visit(url: string, visitTimeout=15000) {
        await this.#page!.goto(url, {
            waitUntil: 'networkidle0',
            timeout: visitTimeout
        });
    }

    public addInterceptor(intercept: RequestInterceptor) {
        this.#requestInterceptors.push(intercept);
    }

    public shield(timeout: number = 5000) {
        const handler: RequestInterceptor = request => {
            const validator = new URLValidator(request.url());
            // Validate url
            if(!validator.scheme(['http', 'https'])) {
                throw new Error('Invalid scheme, only http[s] are accepted');  // TODO: custom error type
            }

            return true;
        }

        this.addInterceptor(handler);
        this.#timeout = setTimeout(async () => {
            await this.close();
        }, timeout);
    }

    public enableDebug() {
        this.#page!.on("console", msg => console.log("PAGE LOG:", msg.text()));
    }

    public async close() {
        this.#timeout && clearTimeout(this.#timeout);
        await this.#page?.close();
        await this.#context?.close();

        this.#page = null;
        this.#context = null;
        this.#timeout = null;
    }

    public async clean() {
        await this.close();
        await this.init();
    }
}

export async function getBrowser(options?: puppeteer.LaunchOptions) {
    return puppeteer.launch(options);
}