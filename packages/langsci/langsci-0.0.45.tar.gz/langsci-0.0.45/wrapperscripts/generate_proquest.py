import yaml
import sys
from datetime import date
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from langsci.catalog.langscipressorg_webcrawler import (
        get_blurb,
        get_soup,
        get_publication_date,
        get_citeinfo,
        get_ISBN_digital,
        get_ISBN_hardcover,
        get_biosketches,
        get_title_subtitle,
        biosketches2names,
    )
from langsci.catalog.catalogmetadata import LICENSES, SERIES, METALANGUAGE


book_ID = sys.argv[1]
soup = get_soup(book_ID)
citegroups = get_citeinfo(soup)
if citegroups is None:
    sys.exit()
print(book_ID)

title, subtitle = get_title_subtitle(citegroups)

series = citegroups["series"]

seriesnumber = citegroups["seriesnumber"]

publication_date = get_publication_date(soup).replace("-", "")
blurb = get_blurb(soup)
try:
  isbn_digital = get_ISBN_digital(soup)
  isbn_print = get_ISBN_hardcover(soup)
except KeyError:
  print(' no ISBN. Skipping')
  sys.exit()
issn = SERIES[citegroups["series"]]
metalanguage = METALANGUAGE.get(book_ID, "eng")

biosketches = get_biosketches(soup)

bisac = "LAN009000"
wgs = "9561"
if series == "Translation and Multilingual Natural Language Processing":
    bisac = "LAN023000"

license = LICENSES.get(book_ID, "CC-BY")
license_url = "https://creativecommons.org/licenses/%s/4.0" % license[3:]
authorrolecode = "A01"
editorrolecode = "B01"

role = authorrolecode
if citegroups["ed"]:
    role = editorrolecode


# FIXME mix of authors and editors


proquest_creator_template = """<Contributor>
        <SequenceNumber>%s</SequenceNumber>
        <ContributorRole>%s</ContributorRole>
        <NamesBeforeKey>%s</NamesBeforeKey>
        <KeyNames>%s</KeyNames>
        <BiographicalNote>%s</BiographicalNote>
</Contributor>"""


creators = []

creatorlist = biosketches2names(biosketches)

for i, creator in enumerate(creatorlist):
    firstname = creator[0]
    lastname = creator[1]
    sketch = creator[2]
    creators.append(
        proquest_creator_template
        % (i + 1, role, escape(firstname), escape(lastname), escape(sketch))
    )
creatorstring = "\n".join(creators)

# creatorstring = authorstring + editorstring
today = date.today().strftime("%Y%m%d")


proquest_template = f"""<?xml version="1.0"?>
<ONIXMessage release="3.0">
  <Header>
    <Sender>
      <SenderIdentifier>
        <SenderIDType>05</SenderIDType>
        <IDValue>978-3-98554</IDValue>
      </SenderIdentifier>
      <SenderName>Language Science Press</SenderName>
      <ContactName>Sebastian Nordhoff</ContactName>
      <EmailAddress>support@langsci-press.org</EmailAddress>
    </Sender>
    <Addressee>
      <AddresseeName>ProQuest</AddresseeName>
    </Addressee>
    <SentDateTime>{today}</SentDateTime>
  </Header>
  <Product>
    <RecordReference>langsci-press.org/{book_ID}</RecordReference>
    <NotificationType>03</NotificationType>
    <RecordSourceType>01</RecordSourceType>
    <RecordSourceIdentifier>
      <RecordSourceIDType>05</RecordSourceIDType>
      <IDValue>978-3-98554</IDValue>
    </RecordSourceIdentifier>
    <RecordSourceName>Language Science Press</RecordSourceName>
    <ProductIdentifier>
      <ProductIDType>06</ProductIDType>
      <IDValue>{citegroups["doi"]}</IDValue>
    </ProductIdentifier>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>{isbn_digital}</IDValue>
    </ProductIdentifier>
    <DescriptiveDetail>
      <!-- P.3 -->
      <ProductComposition>00</ProductComposition>
      <ProductForm>ED</ProductForm>
      <!-- <EpubType>002</EpubType> -->
      <!--
      <Measure>
        <MeasureType>01</MeasureType>
        <Measurement>24.00</Measurement>
        <MeasureUnitCode>cm</MeasureUnitCode>
      </Measure>
      <Measure>
        <MeasureType>02</MeasureType>
        <Measurement>17.00</Measurement>
        <MeasureUnitCode>cm</MeasureUnitCode>
      </Measure>
      -->
      <Collection>
        <CollectionType>10</CollectionType>
        <CollectionIdentifier>
          <CollectionIDType>02</CollectionIDType>
          <IDValue>{issn}</IDValue>
        </CollectionIdentifier>
        <CollectionSequence>
          <CollectionSequenceType>02</CollectionSequenceType>
          <CollectionSequenceNumber>9</CollectionSequenceNumber>
        </CollectionSequence>
        <TitleDetail>
          <TitleType>01</TitleType>
          <TitleElement>
            <TitleElementLevel>02</TitleElementLevel>
            <TitleText textcase="02">{series}</TitleText>
          </TitleElement>
        </TitleDetail>
      </Collection>
      <TitleDetail>
        <TitleType>01</TitleType>
        <TitleElement>
          <TitleElementLevel>01</TitleElementLevel>
          <TitleText textcase="01">{title}</TitleText>
          <Subtitle>{subtitle}</Subtitle>
        </TitleElement>
      </TitleDetail>
      {creatorstring}
      <EditionNumber>1</EditionNumber>
      <Language>
        <LanguageRole>01</LanguageRole>
        <LanguageCode>{metalanguage}</LanguageCode>
      </Language>
      <Subject>
        <MainSubject />
        <SubjectSchemeIdentifier>10</SubjectSchemeIdentifier>
        <SubjectSchemeVersion>2009</SubjectSchemeVersion>
        <SubjectCode>{bisac}</SubjectCode>
      </Subject>
      <Subject>
        <MainSubject />
        <SubjectSchemeIdentifier>26</SubjectSchemeIdentifier>
        <SubjectSchemeVersion>2.0</SubjectSchemeVersion>
        <SubjectCode>{wgs}</SubjectCode>
      </Subject>
      <AudienceCode>06</AudienceCode>
      <EpubLicense>
        <EpubLicenseExpression>
          <EpubLicenseExpressionLink>{license_url.lower()}</EpubLicenseExpressionLink>
        </EpubLicenseExpression>
      </EpubLicense>
    </DescriptiveDetail>
    <CollateralDetail>
      <TextContent>
        <TextType>03</TextType>
        <Text textformat="05">
          {escape(blurb)}
        </Text>
      </TextContent>
      <SupportingResource>
        <ResourceContentType>01</ResourceContentType>
        <ContentAudience>00</ContentAudience>
        <ResourceMode>03</ResourceMode>
        <ResourceVersion>
          <ResourceForm>02</ResourceForm>
          <ResourceVersionFeature>
            <ResourceVersionFeatureType>01</ResourceVersionFeatureType>
            <FeatureValue>D503</FeatureValue>
          </ResourceVersionFeature>
          <ResourceLink>https://langsci-press.org/$$$call$$$/submission/cover/cover?submissionId={book_ID}</ResourceLink>
        </ResourceVersion>
      </SupportingResource>
      <TextContent>
        <TextType>20</TextType>
        <Text>This text is licensed as {license} 4.0</Text>
      </TextContent>
    </CollateralDetail>
    <PublishingDetail>
      <Publisher>
        <PublishingRole>01</PublishingRole>
        <PublisherName>Language Science Press</PublisherName>
        <Website>
          <WebsiteRole>01</WebsiteRole>
          <WebsiteLink>https://www.langsci-press.org</WebsiteLink>
        </Website>
      </Publisher>
      <CityOfPublication>Berlin</CityOfPublication>
      <CountryOfPublication>DE</CountryOfPublication>
      <PublishingStatus>04</PublishingStatus>
      <PublishingDate>
        <PublishingDateRole>01</PublishingDateRole>
        <Date dateformat="00">{publication_date}</Date>
      </PublishingDate>
    </PublishingDetail>
    <ProductSupply>
      <SupplyDetail>
        <UnpricedItemType>01</UnpricedItemType>
      </SupplyDetail>
    </ProductSupply>
    <othertext>
            <d102>20</d102>
            <d103>06</d103>
            <d104>Der Titel ist Open Access unter der Creative Commons Lizenz {license} 4.0</d104>
  </othertext>
    <othertext>
            <d102>46</d102>
            <d103>01</d103>
            <d104>{license_url.lower()}</d104>
  </othertext>
  <OtherText>
    <TextTypeCode>47</TextTypeCode>
    <TextFormat>06</TextFormat>
    <Text>Open access </Text>
  </OtherText>
  </Product>
</ONIXMessage>"""

onix2_template = f"""<?xml version="1.0"?>
<ONIXMessage xmlns="http://www.editeur.org/onix/2.1">
  <Header>
    <Sender>
      <SenderIdentifier>
        <SenderIDType>05</SenderIDType>
        <IDValue>978-3-98554</IDValue>
      </SenderIdentifier>
      <SenderName>Language Science Press</SenderName>
      <ContactName>Sebastian Nordhoff</ContactName>
      <EmailAddress>support@langsci-press.org</EmailAddress>
    </Sender>
    <Addressee>
      <AddresseeName>ProQuest</AddresseeName>
    </Addressee>
    <SentDateTime>{today}</SentDateTime>
  </Header>
  <Product>
    <RecordReference>langsci-press.org/{book_ID}</RecordReference>
    <NotificationType>03</NotificationType>
    <RecordSourceType>01</RecordSourceType>
    <RecordSourceIdentifier>
      <RecordSourceIDType>05</RecordSourceIDType>
      <IDValue>978-3-98554</IDValue>
    </RecordSourceIdentifier>
    <RecordSourceName>Language Science Press</RecordSourceName>
    <ProductIdentifier>
      <ProductIDType>06</ProductIDType>
      <IDValue>{citegroups["doi"]}</IDValue>
    </ProductIdentifier>
    <ProductIdentifier>
      <ProductIDType>15</ProductIDType>
      <IDValue>{isbn_digital}</IDValue>
    </ProductIdentifier>
    <DescriptiveDetail>
      <!-- P.3 -->
      <ProductComposition>00</ProductComposition>
      <ProductForm>ED</ProductForm>
      <Collection>
        <CollectionType>10</CollectionType>
        <CollectionIdentifier>
          <CollectionIDType>02</CollectionIDType>
          <IDValue>{issn}</IDValue>
        </CollectionIdentifier>
        <CollectionSequence>
          <CollectionSequenceType>02</CollectionSequenceType>
          <CollectionSequenceNumber>9</CollectionSequenceNumber>
        </CollectionSequence>
        <TitleDetail>
          <TitleType>01</TitleType>
          <TitleElement>
            <TitleElementLevel>02</TitleElementLevel>
            <TitleText>{series}</TitleText>
          </TitleElement>
        </TitleDetail>
      </Collection>
      <TitleDetail>
        <TitleType>01</TitleType>
        <TitleElement>
          <TitleElementLevel>01</TitleElementLevel>
          <TitleText>{title}</TitleText>
          <Subtitle>{subtitle}</Subtitle>
        </TitleElement>
      </TitleDetail>
      {creatorstring}
      <EditionNumber>1</EditionNumber>
      <Language>
        <LanguageRole>01</LanguageRole>
        <LanguageCode>{metalanguage}</LanguageCode>
      </Language>
      <Subject>
        <MainSubject />
        <SubjectSchemeIdentifier>10</SubjectSchemeIdentifier>
        <SubjectSchemeVersion>2009</SubjectSchemeVersion>
        <SubjectCode>{bisac}</SubjectCode>
      </Subject>
      <Subject>
        <MainSubject />
        <SubjectSchemeIdentifier>26</SubjectSchemeIdentifier>
        <SubjectSchemeVersion>2.0</SubjectSchemeVersion>
        <SubjectCode>{wgs}</SubjectCode>
      </Subject>
      <AudienceCode>06</AudienceCode>
      <EpubLicense>
        <EpubLicenseExpression>
          <EpubLicenseExpressionLink>{license_url.lower()}</EpubLicenseExpressionLink>
        </EpubLicenseExpression>
      </EpubLicense>
    </DescriptiveDetail>
    <CollateralDetail>
      <TextContent>
        <TextType>03</TextType>
        <Text textformat="05">
          {escape(blurb)}
        </Text>
      </TextContent>
      <SupportingResource>
        <ResourceContentType>01</ResourceContentType>
        <ContentAudience>00</ContentAudience>
        <ResourceMode>03</ResourceMode>
        <ResourceVersion>
          <ResourceForm>02</ResourceForm>
          <ResourceVersionFeature>
            <ResourceVersionFeatureType>01</ResourceVersionFeatureType>
            <FeatureValue>D503</FeatureValue>
          </ResourceVersionFeature>
          <ResourceLink>https://langsci-press.org/$$$call$$$/submission/cover/cover?submissionId={book_ID}</ResourceLink>
        </ResourceVersion>
      </SupportingResource>
      <TextContent>
        <TextType>20</TextType>
        <Text>This text is licensed as {license} 4.0</Text>
      </TextContent>
    </CollateralDetail>
    <PublishingDetail>
      <Publisher>
        <PublishingRole>01</PublishingRole>
        <PublisherName>Language Science Press</PublisherName>
        <Website>
          <WebsiteRole>01</WebsiteRole>
          <WebsiteLink>https://www.langsci-press.org</WebsiteLink>
        </Website>
      </Publisher>
      <CityOfPublication>Berlin</CityOfPublication>
      <CountryOfPublication>DE</CountryOfPublication>
      <PublishingStatus>04</PublishingStatus>
      <PublishingDate>
        <PublishingDateRole>01</PublishingDateRole>
        <Date>{publication_date}</Date>
      </PublishingDate>
    </PublishingDetail>
    <ProductSupply>
      <SupplyDetail>
        <UnpricedItemType>01</UnpricedItemType>
      </SupplyDetail>
    </ProductSupply>
    <OtherText>
      <TextTypeCode>47</TextTypeCode>
      <TextFormat>06</TextFormat>
      <Text>Open access </Text>
    </OtherText>
  </Product>
</ONIXMessage>
"""


onix3_template = f"""<?xml version="1.0"?>
<ONIXmessage release="3.0">

<Header>
  <sender>
    <SenderName>Language Science Press</SenderName>
    <ContactName>Sebastian Nordhoff</ContactName>
    <EmailAddress>support@langsci-press.org</EmailAddress>
  </sender>
    <SentDateTime>{today}</SentDateTime>
</Header>

<Product>
  <RecordReference>langsci-press.org/{book_ID}</RecordReference>
  <NotificationType>03</NotificationType>
  <RecordSourceType>01</RecordSourceType>
  <RecordSourceIdentifier>
    <RecordSourceIDType>05</RecordSourceIDType>
    <IDValue>978-3-98554</IDValue>
  </RecordSourceIdentifier>
  <RecordSourceName>Language Science Press</RecordSourceName>

  <ProductIdentifier>
    <ProductIDType>15</ProductIDType>
    <IDTypeName>{isbn_digital}</IDTypeName>
    <ProductForm> EA </ProductForm>
    <ProductFormDetail> E107 </ProductFormDetail>
  </ProductIdentifier>

  <PrimaryContentType> 10 </PrimaryContentType>

  <ProductFormfeature>
    <ProductFormFeatureType> 09  </ProductFormFeatureType>
    <ProductFormFeatureValue> 11 </ProductFormFeatureValue>
  </ProductFormfeature>

  <ProductFormfeature>
    <ProductFormFeatureType> 09  </ProductFormFeatureType>
    <ProductFormFeatureValue> 12 </ProductFormFeatureValue>
  </ProductFormfeature>

  <ProductFormfeature>
    <ProductFormFeatureType> 09  </ProductFormFeatureType>
    <ProductFormFeatureValue> 25 </ProductFormFeatureValue>
  </ProductFormfeature>

  <ProductFormfeature>
    <ProductFormFeatureType> 12</ProductFormFeatureType>
    <ProductFormFeatureValue> 00</ProductFormFeatureValue>
  </ProductFormfeature>

  <DescriptiveDetail>
    <ProductComposition>00</ProductComposition>
    <ProductForm>ED</ProductForm>
    <!-- <EpubType>002</EpubType> -->
    <Measure>
      <MeasureType>01</MeasureType>
      <Measurement>24.00</Measurement>
      <MeasureUnitCode>cm</MeasureUnitCode>
    </Measure>
    <Measure>
      <MeasureType>02</MeasureType>
      <Measurement>17.00</Measurement>
      <MeasureUnitCode>cm</MeasureUnitCode>
    </Measure>

    <Collection>
      <CollectionType>10</CollectionType>
      <CollectionIdentifier>
        <CollectionIDType>02</CollectionIDType>
        <IDValue>{issn}</IDValue>
      </CollectionIdentifier>
      <CollectionSequence>
        <CollectionSequenceType>02</CollectionSequenceType>
      <CollectionSequenceNumber>{seriesnumber}</CollectionSequenceNumber>
      </CollectionSequence>
      <TitleDetail>
        <TitleType>01</TitleType>
        <TitleElement>
          <TitleElementLevel>02</TitleElementLevel>
          <TitleText textcase="02">{series}</TitleText>
        </TitleElement>
      </TitleDetail>
    </Collection>

    <TitleDetail>
      <TitleType>01</TitleType>
      <TitleElement>
        <TitleElementLevel>01</TitleElementLevel>
        <TitleText textcase="01">{title}</TitleText>
        <Subtitle>{subtitle}</Subtitle>
      </TitleElement>
    </TitleDetail>

    {creatorstring}

    <EditionNumber>1</EditionNumber>

    <Language>
      <LanguageRole>01</LanguageRole>
      <LanguageCode>{metalanguage}</LanguageCode>
    </Language>

    <Subject>
      <MainSubject />
      <SubjectSchemeIdentifier>10</SubjectSchemeIdentifier>
      <SubjectSchemeVersion>2009</SubjectSchemeVersion>
      <SubjectCode>{bisac}</SubjectCode>
    </Subject>

    <Subject>
      <MainSubject />
      <SubjectSchemeIdentifier>26</SubjectSchemeIdentifier>
      <SubjectSchemeVersion>2.0</SubjectSchemeVersion>
      <SubjectCode>{wgs}</SubjectCode>
    </Subject>

    <AudienceCode>06</AudienceCode>

    <EpubLicense>
      <EpubLicenseExpression>
        <EpubLicenseExpressionLink>{license_url.lower()}</EpubLicenseExpressionLink>
      </EpubLicenseExpression>
    </EpubLicense>
  </DescriptiveDetail>
   <CollateralDetail>
      <TextContent>
        <TextType>03</TextType>
        <ContentAudience> 00  </ContentAudience>
        <Text textformat="05">
          {escape(blurb)}
        </Text>
      </TextContent>
      <Imprint>
        <ImprintName> Language Science Press</ImprintName>
      </Imprint>
      <SupportingResource>
        <ResourceContentType>01</ResourceContentType>
        <ContentAudience>00</ContentAudience>
        <ResourceMode>03</ResourceMode>
        <ResourceVersion>
          <ResourceForm>02</ResourceForm>
          <ResourceVersionFeature>
            <ResourceVersionFeatureType>01</ResourceVersionFeatureType>
            <FeatureValue>D503</FeatureValue>
          </ResourceVersionFeature>
          <ResourceLink>https://langsci-press.org/$$$call$$$/submission/cover/cover?submissionId={book_ID}</ResourceLink>
        </ResourceVersion>
      </SupportingResource>
      <TextContent>
        <TextType>20</TextType>
        <Text>This text is licensed as {license} 4.0</Text>
      </TextContent>
    </CollateralDetail>
    <PublishingDetail>
      <Publisher>
        <PublishingRole>01</PublishingRole>
        <PublisherName>Language Science Press</PublisherName>
        <PublisherIdentifier>
          <PublisherIDType> 05 </PublisherIDType>
          <IDValue> 978-3-98554</IDValue>
        </PublisherIdentifier>
        <Website>
          <WebsiteRole>01</WebsiteRole>
          <WebsiteLink>https://www.langsci-press.org</WebsiteLink>
        </Website>
        <PublishingStatus>04</PublishingStatus>
        <CityOfPublication>Berlin</CityOfPublication>
        <CountryOfPublication>DE</CountryOfPublication>
      </Publisher>
      <PublishingDate>
        <PublishingDateRole>01</PublishingDateRole>
        <Date dateformat="00">{publication_date}</Date>
      </PublishingDate>
    </PublishingDetail>
    <ProductSupply>
      <SupplyDetail>
        <UnpricedItemType>01</UnpricedItemType>
      </SupplyDetail>
    </ProductSupply>
    <othertext>
            <d102>20</d102>
            <d103>06</d103>
            <d104>Der Titel ist Open Access unter der Creative Commons Lizenz {license} 4.0</d104>
    </othertext>
    <othertext>
            <d102>46</d102>
            <d103>01</d103>
            <d104>{license_url.lower()}</d104>
    </othertext>
    <OtherText>
      <TextTypeCode>47</TextTypeCode>
      <TextFormat>06</TextFormat>
      <Text>Open access </Text>
    </OtherText>
    <copyrightstatement>
      <CopyrightType> C </CopyrightType>
      <CopyrightYear> {publication_date[:4]} </CopyrightYear>
    </copyrightstatement>
    <RelatedProduct>
      <RelationCode> 13 </RelationCode>
      <ProductIdentifier>
        <ProductIDType> 15</ProductIDType>
        <IDValue> {isbn_print} </IDValue>
        <ProductForm> BB </ProductForm>
      </ProductIdentifier>
    </RelatedProduct>
  </Product>
</ONIXmessage>

"""

with open(f"proquest_onix3/{isbn_digital}.xml", "w") as xmlout:
    # validate XML
    # ET.fromstring(proquest_template)
    # xmlout.write(proquest_template)
    # print(onix3_template)
    ET.fromstring(onix3_template)
    xmlout.write(onix3_template)
