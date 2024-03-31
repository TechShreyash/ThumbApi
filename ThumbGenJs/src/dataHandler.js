// kfhsfjahf
// Replace with your actual values
const apiKey = 'dzhlNuyl6Cbypq1T15wPF8lyG3tsQKZkTF9MoVZSlxRX6zw37qi56lm9yKuM14z8';
const database = 'AnimeThumb';
const collection1 = 'ThumbUrls';
const collection2 = "WebsiteViews"

// Function to update a record by ID
async function updateRecord(id, updateData, collection = collection1) {
    const url = 'https://ap-south-1.aws.data.mongodb-api.com/app/data-bsnjq/endpoint/data/v1/action/updateOne'
    const data = JSON.stringify({
        "collection": collection,
        "database": database,
        "dataSource": "WebsiteData",
        "filter": { "id": id },
        "update": updateData,
        "upsert": true
    });

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': apiKey,
        },
        body: data,
    });
    const result = await response.json();
}

// Function to get a record by ID
async function getRecord(id) {
    console.log('getRecord', id);
    const url = 'https://ap-south-1.aws.data.mongodb-api.com/app/data-bsnjq/endpoint/data/v1/action/findOne';
    const data = JSON.stringify({
        "collection": collection1,
        "database": database,
        "dataSource": "WebsiteData",
        "filter": {
            "id": id
        }
    });

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': apiKey,
        },
        body: data,
    });

    if (!response.ok) {
        console.log('getRecord', await response.text());
        throw new Error(`Get record failed with status: ${response.status}`);
    }

    const record = await response.json();
    return record['document'];
}

async function add_Large_DB(id, large) {
    await updateRecord(id, {
        "$set": { "large": large }
    });
}

async function add_Thumb_DB(id, thumb) {
    await updateRecord(id, {
        "$set": { "thumb": thumb }
    });

}

async function search_in_DB(id) {
    const data = await getRecord(id);
    if (data == null) {
        return { large: null, thumb: null };
    }
    else {
        return data;
    }
}

export { add_Large_DB, add_Thumb_DB, search_in_DB };
