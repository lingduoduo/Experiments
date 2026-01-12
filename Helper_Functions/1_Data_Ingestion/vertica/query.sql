with conv as (SELECT cv.ID,
                     cv.CONV_TIME_STAMP,
                     cv.click_id,
                     cc.AMP_CLICK_TIMESTAMP,
                     CASE
                         WHEN cv.pixel_id IS NULL THEN NULL
                         ELSE (CASE WHEN cv.order_value >= 0 THEN cv.order_value ELSE 0 END) END           AS order_value,
                     CASE
                         WHEN cv.pixel_id IS NULL THEN NULL
                         ELSE ROW_NUMBER() OVER (PARTITION BY cv.click_id ORDER BY cv.conv_time_stamp) END AS opc_rank,
                     CASE
                         WHEN cv.pixel_id IS NULL THEN NULL
                         ELSE ROW_NUMBER()
                              OVER (PARTITION BY cv.click_id, cv.pixel_id ORDER BY cv.conv_time_stamp) END AS opcpe_rank
              FROM clickcache.conversion cv
                       JOIN clickcache.click cc ON cc.id = cv.click_id
                       JOIN ampx.ACCOUNT a on a.ID = cc.ADV_ACCOUNT_ID
                       JOIN
                   (SELECT DISTINCT campaign_id, conversion_pixel_id
                    FROM ampx.campaign_event_funnel
                    where include_reporting = 1) ef
                   ON ef.campaign_id = cc.adv_campaign_id AND ef.conversion_pixel_id = cv.pixel_id
              WHERE cc.AMP_CLICK_DAY  between CURRENT_DATE() - 180 and CURRENT_DATE() - 1
                AND ((CONV_WINDOW_MINUTES IS NULL) OR (CONV_WINDOW_MINUTES is not null AND
                                                       TIMESTAMPDIFF(MINUTE, cc.AMP_CLICK_TIMESTAMP, cv.CONV_TIME_STAMP) <=
                                                       CONV_WINDOW_MINUTES))
                And cc.AMP_CLICK_STATUS_ID in (1, 5, 7, 14, 19, 51)),
cv as (select conv.ID,
                     conv.CONV_TIME_STAMP,
                     conv.click_id,
                     conv.AMP_CLICK_TIMESTAMP,
                     conv.order_value
            from clickcache.click cc
                     join ampx.CAMPAIGN ca on ca.ID = cc.ADV_CAMPAIGN_ID
                     join conv on conv.click_id = cc.ID and conv.AMP_CLICK_TIMESTAMP = cc.AMP_CLICK_TIMESTAMP
                     left join ampx.GEO_COUNTRIES gc on CASE
                                                            WHEN CC.PUB_PUBLISHER_ID = 12497 AND CC.PUB_SUB_2 <> 'uk'
                                                                THEN upper(CC.PUB_SUB_2) = gc.COUNTRY_CODE
                END
            where cc.AMP_CLICK_DAY between current_date() - 180 and CURRENT_DATE() - 1 --change here
              and cc.ADV_ACCOUNT_ID = 74521
              and cc.USR_GEO_COUNTRY_ID = 2
              and cc.PUB_PUBLISHER_ID in
                  (select distinct PUBLISHER_ID
                   from publisher_taxonomy.PUBLISHER_MEDIA_TAXONOMY
                   where MEDIA_PRODUCT_ID = 10)),
click as (select cc.ID                                                                        as click_id,
                      cc.AMP_CLICK_TIMESTAMP                                                      as AMP_CLICK_TIMESTAMP,
                      cc.AMP_CLICK_DAY                                                            as AMP_CLICK_DAY,
                      cc.ADV_ACCOUNT_ID                                                           as ACCOUNT_ID,
                      cc.ADV_CAMPAIGN_ID                                                          as CAMPAIGN_ID,
                      cc.ADV_ADGROUP_ID                                                           as ADGROUP_ID,
                      cc.ADV_KEYWORD_ID                                                           as KEYWORD_ID,
                      cc.ADV_CREATIVE_ID                                                          as CREATIVE_ID,
                      cc.ADV_ADCOPY_ID                                                            as ADCOPY_ID,
                      cc.PUB_PUBLISHER_ID                                                         as PUBLISHER_ID,
                      cc.PUB_ATS_ID                                                               as PUB_ATS_ID,
                      cc.PUB_PLACEMENT_ID                                                         as PLACEMENT_ID,
                      cc.USR_DEVICE_GROUP_ID                                                      as DEVICE_GROUP_ID,
                      cc.USR_DEVICE_TYPE_ID                                                       as DEVICE_TYPE_ID,
                      cc.PUB_SUB_1                                                                as PUB_SUB_1,
                      cc.PUB_SUB_2                                                                as PUB_SUB_2,
                      CASE
                          WHEN CC.PUB_PUBLISHER_ID = 12497 AND CC.PUB_SUB_2 = 'uk' then 1
                          WHEN CC.PUB_PUBLISHER_ID = 12497 AND CC.PUB_SUB_2 <> 'uk' then gc.ID
                          ELSE cc.USR_GEO_COUNTRY_ID end                                          as COUNTRY_ID,
                      cc.USR_GEO_REGION_ID                                                        as REGION_ID,
                      cc.USR_GEO_CITY_ID                                                          as CITY_ID,
                      cc.USR_GEO_DMA_CODE                                                         as DMA_CODE,
                      case when cc.AMP_CLICK_STATUS_ID = 1 then cc.ADV_CPC else 0 end            as spend,
                      case when cc.AMP_CLICK_STATUS_ID in (1, 51) then cc.PUB_CPC else 0 end     as publisher_payout,
                      case when cc.AMP_CLICK_STATUS_ID = 1 then 1 else 0 end                     as valid_clicks,
                      case when cc.AMP_CLICK_STATUS_ID = 51 then 1 else 0 end                    as onboarding_clicks,
                      case when cc.AMP_CLICK_STATUS_ID not in (1, 51) then 1 else 0 end          as invalid_clicks
               from clickcache.click cc
                    left join ampx.GEO_COUNTRIES gc on CASE
                    WHEN CC.PUB_PUBLISHER_ID = 12497 AND CC.PUB_SUB_2 <> 'uk'
                    THEN upper(CC.PUB_SUB_2) = gc.COUNTRY_CODE
                   END
                where cc.AMP_CLICK_DAY  between CURRENT_DATE() - 180 and CURRENT_DATE() - 1
                  and cc.ADV_ACCOUNT_ID = 74521
                  and cc.USR_GEO_COUNTRY_ID = 2
                  and cc.PUB_PUBLISHER_ID in
                      (select distinct PUBLISHER_ID
                       from publisher_taxonomy.PUBLISHER_MEDIA_TAXONOMY
                       where MEDIA_PRODUCT_ID = 10)),
cc_cv as (
select cc.click_id,
        cc.AMP_CLICK_TIMESTAMP,
        hour(cc.AMP_CLICK_TIMESTAMP) AS AMP_CLICK_HOUR,
        cc.AMP_CLICK_DAY,
        cc.ACCOUNT_ID,
        cc.CAMPAIGN_ID,
        cc.ADGROUP_ID,
        cc.KEYWORD_ID,
        cc.CREATIVE_ID,
        cc.ADCOPY_ID,
        cc.PUBLISHER_ID,
        cc.PUB_ATS_ID,
        cc.PLACEMENT_ID,
        cc.DEVICE_GROUP_ID,
        cc.DEVICE_TYPE_ID,
        cc.PUB_SUB_1,
        cc.PUB_SUB_2,
        cc.COUNTRY_ID,
        cc.REGION_ID,
        cc.CITY_ID,
        cc.DMA_CODE,
        cc.spend,
        cc.publisher_payout,
        cc.valid_clicks,
        cc.onboarding_clicks,
        cc.invalid_clicks,
        cv.ID,
        cv.CONV_TIME_STAMP,
        cv.order_value
     from click cc
     left join cv on cc.click_id = cv.click_id and cc.AMP_CLICK_TIMESTAMP = cv.AMP_CLICK_TIMESTAMP
),
conv_agg as (
SELECT case when random() < 0.2 then 1 else 0 end as holdout,
        1 as conversion,
        AMP_CLICK_DAY,
        AMP_CLICK_HOUR,
        ACCOUNT_ID,
        CAMPAIGN_ID,
        ADGROUP_ID,
        KEYWORD_ID,
        CREATIVE_ID,
        ADCOPY_ID,
        PUBLISHER_ID,
        PUB_ATS_ID,
        PLACEMENT_ID,
        DEVICE_GROUP_ID,
        DEVICE_TYPE_ID,
        PUB_SUB_1,
        PUB_SUB_2,
        COUNTRY_ID,
        REGION_ID,
        CITY_ID,
        DMA_CODE,
        sum(IFNULL(spend, 0))                         as SPEND,
        sum(IFNULL(publisher_payout, 0))              as PUBLISHER_PAYOUT,
        sum(IFNULL(valid_clicks, 0))                  as VALID_CLICKS,
        sum(IFNULL(onboarding_clicks, 0))             as ONBOARDING_CLICKS,
        sum(IFNULL(invalid_clicks, 0))                as INVALID_CLICKS,
        sum(IFNULL(order_value, 0))                   as order_value
FROM cc_cv
WHERE ID is not NULL
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
),
nonconv_agg as (
SELECT case when random() < 0.2 then 1 else 0 end as holdout,
        0 as conversion,
        AMP_CLICK_DAY,
        AMP_CLICK_HOUR,
        ACCOUNT_ID,
        CAMPAIGN_ID,
        ADGROUP_ID,
        KEYWORD_ID,
        CREATIVE_ID,
        ADCOPY_ID,
        PUBLISHER_ID,
        PUB_ATS_ID,
        PLACEMENT_ID,
        DEVICE_GROUP_ID,
        DEVICE_TYPE_ID,
        PUB_SUB_1,
        PUB_SUB_2,
        COUNTRY_ID,
        REGION_ID,
        CITY_ID,
        DMA_CODE,
        sum(IFNULL(spend, 0))                         as SPEND,
        sum(IFNULL(publisher_payout, 0))              as PUBLISHER_PAYOUT,
        sum(IFNULL(valid_clicks, 0))                  as VALID_CLICKS,
        sum(IFNULL(onboarding_clicks, 0))             as ONBOARDING_CLICKS,
        sum(IFNULL(invalid_clicks, 0))                as INVALID_CLICKS,
        sum(IFNULL(order_value, 0))                   as order_value
FROM cc_cv
WHERE ID is NULL
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
)
SELECT * FROM conv_agg
UNION ALL
SELECT * FROM nonconv_agg