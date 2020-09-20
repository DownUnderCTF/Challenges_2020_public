import { URL } from "url";

export class URLValidator {
    public static readonly ALLOWED_SCHEMES = ["http", "https"];
    public static readonly INTERNAL_CIDR = [];

    #url: URL;
    constructor(url: string) {
        this.#url = new URL(url);
    }

    public scheme(validSchemes: string[] = URLValidator.ALLOWED_SCHEMES) {
        return validSchemes.some(scheme => scheme+':' == this.#url.protocol.toLowerCase());
    }

    public externalIP() {

    }
}