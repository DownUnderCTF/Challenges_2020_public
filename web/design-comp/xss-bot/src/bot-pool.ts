import { BotController } from "./bot";
import { Browser } from "puppeteer";
import genericPool from "generic-pool";

export function createPool(browser: Browser, opts?: genericPool.Options) {
    return genericPool.createPool({
        async create() {
            const bot = new BotController(browser);
            await bot.init();
            return bot;
        },
        async destroy(rsrc: BotController) {
            await rsrc.close();
        }
    }, opts || {max: 16, min: 2});
}