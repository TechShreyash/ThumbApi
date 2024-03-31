// For Fixing CORS issue
// CORS Fix Start

const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, HEAD, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
};

function handleOptions(request) {
    if (
        request.headers.get("Origin") !== null &&
        request.headers.get("Access-Control-Request-Method") !== null &&
        request.headers.get("Access-Control-Request-Headers") !== null
    ) {
        return new Response(null, {
            headers: corsHeaders,
        });
    } else {
        return new Response(null, {
            headers: {
                Allow: "GET, HEAD, POST, OPTIONS",
            },
        });
    }
}

// CORS Fix End

import { add_Large_DB, add_Thumb_DB, search_in_DB } from "./dataHandler.js";
import { GenerateImage, GenerateThumbnail } from "./thumbHandler.js";
import { increaseViews } from "./statsHandler.js"

const AvailableImages = {};
const AvailableThumbs = {};

export default {
    async fetch(request, env, ctx) {
        if (request.method === "OPTIONS") {
            // Handle CORS preflight requests
            return handleOptions(request);
        } else if (
            request.method === "GET" ||
            request.method === "HEAD" ||
            request.method === "POST"
        ) {
            const url = request.url;

            if (url.includes("/get/")) {
                const headers = request.headers;

                let episodeId = url.split("/get/")[1];
                if (episodeId.includes("?")) {
                    episodeId = episodeId.split("?")[0];
                }

                if (episodeId === 'null-episode-null' || episodeId === null || episodeId === undefined) throw new Error('Invalid Episode ID');

                // Check if in AvailableImages variable
                let data = AvailableImages[episodeId];
                if (data !== undefined && data !== null) {
                    await increaseViews(headers);
                    return Response.redirect(data, 301);
                }

                // Check if url in db
                const dbdata = await search_in_DB(episodeId);
                if (dbdata.large !== undefined && dbdata.large !== null) {
                    AvailableImages[episodeId] = dbdata.large;
                    await increaseViews(headers);
                    console.log(dbdata.large)

                    return Response.redirect(dbdata.large, 301);
                }

                // If not in db then generate new thumbnail
                data = await GenerateImage(episodeId);

                if (data === false) {
                    throw "Something went wrong";
                } else {
                    AvailableImages[episodeId] = data.large;
                    await add_Large_DB(episodeId, data.large);
                    await increaseViews(headers);

                    return Response.redirect(data.large, 301);
                }
            } else if (url.includes("/thumb/")) {
                const headers = request.headers;

                let episodeId = url.split("/thumb/")[1];
                if (episodeId.includes("?")) {
                    episodeId = episodeId.split("?")[0];
                }

                if (episodeId === 'null-episode-null' || episodeId === null || episodeId === undefined) throw new Error('Invalid Episode ID');

                // Check if in AvailableThumbs variable
                let data = AvailableThumbs[episodeId];
                if (data !== undefined && data !== null) {
                    await increaseViews(headers);

                    return Response.redirect(data, 301);
                }

                // Check if url in db
                const dbdata = await search_in_DB(episodeId);
                if (dbdata.thumb !== undefined && dbdata.thumb !== null) {
                    AvailableThumbs[episodeId] = dbdata.thumb;
                    await increaseViews(headers);

                    return Response.redirect(dbdata.thumb, 301);
                }

                // If not in db then generate new thumbnail
                data = await GenerateThumbnail(episodeId);

                if (data === false) {
                    throw "Something went wrong";
                } else {
                    AvailableThumbs[episodeId] = data.thumb;
                    await add_Thumb_DB(episodeId, data.thumb);
                    await increaseViews(headers);
                    return Response.redirect(data.thumb, 301);
                }
            }

            const text =
                "Api is working fine.\n\nSupport : https://telegram.me/TechZBots_Support";

            return new Response(text, {
                headers: {
                    "content-type": "text/plain",
                    "Access-Control-Allow-Origin": "*",
                    Vary: "Origin",
                },
            });
        } else {
            return new Response(null, {
                status: 405,
                statusText: "Method Not Allowed",
            });
        }
    },
};
