export interface AlphaUser {
    _id?: string;
    _rev?: string;
    custom_RegCompanyName?: string;
    frUnindexedString1?: string;
    frUnindexedString2?: string;
    frUnindexedString3?: string;
    frUnindexedString4?: string;
    frUnindexedString5?: string;
    frIndexedString11?: string;
    frIndexedString12?: string;
    frIndexedString10?: string;
    frIndexedString19?: string;
    frIndexedString17?: string;
    frIndexedString18?: string;
    frIndexedString15?: string;
    frIndexedString16?: string;
    frIndexedString13?: string;
    frIndexedString14?: string;
    givenName?: string;
    frIndexedString20?: string;
    telephoneNumber?: string;
    city?: string;
    displayName?: string;
    accountStatus?: string;
    sn?: string;
    frUnindexedDate1?: string;
    frIndexedString9?: string;
    frIndexedString8?: string;
    frIndexedString7?: string;
    frIndexedString6?: string;
    passwordLastChangedTime?: string;
    country?: string;
    mail?: string;
    frIndexedDate5?: string;
    frIndexedDate4?: string;
    frIndexedDate3?: string;
    frIndexedString5?: string;
    frIndexedString4?: string;
    frIndexedString3?: string;
    frIndexedString2?: string;
    frIndexedString1?: string;
    frUnindexedInteger3?: string;
    frUnindexedInteger2?: string;
    frUnindexedInteger1?: string;
    description?: string;
    frIndexedInteger4?: string;
    frIndexedInteger3?: string;
    frIndexedInteger2?: string;
    frIndexedInteger1?: string;
    frIndexedInteger5?: string;
    userName?: string;
    frIndexedDate2?: string;
    frIndexedDate1?: string;

}

export interface OpenIdmResponse<T> {
    result: T[];
    resultCount: number;
    totalPagedResults: number;
    pagedResultsCookie: string | null;
}