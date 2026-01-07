/// <reference types="vite/client" />

// Google API (gapi) グローバル型定義
declare const gapi: {
    load: (apiName: string, callback: () => void) => void;
    client: {
        init: (config: {
            apiKey?: string;
            clientId: string;
            discoveryDocs?: string[];
            scope: string;
        }) => Promise<void>;
        calendar: {
            events: {
                insert: (params: { calendarId: string; resource: any }) => Promise<{ result: any }>;
            };
        };
        tasks: {
            tasklists: {
                list: () => Promise<{ result: { items?: Array<{ id: string }> } }>;
            };
            tasks: {
                insert: (params: { tasklist: string; resource: any }) => Promise<{ result: any }>;
            };
        };
    };
    auth2: {
        getAuthInstance: () => {
            isSignedIn: {
                get: () => boolean;
                listen: (callback: (isSignedIn: boolean) => void) => void;
            };
            signIn: () => Promise<any>;
            signOut: () => Promise<any>;
            currentUser: {
                get: () => {
                    getBasicProfile: () => {
                        getName: () => string;
                        getEmail: () => string;
                        getImageUrl: () => string;
                    };
                };
            };
        };
    };
};
