from time import sleep, time
from httpx import Client
from requests_toolbelt import MultipartEncoder
import os, secrets, string, random, websocket, json, threading, queue
from loguru import logger
import json, random

QUERIES = {
  "AddEmailMutation": "6d9ff3c8ed7badced30cfdad97492d4c21719931e8c44c5601abfa429b62ded7",
  "ChatHelpers_addMessageBreakEdgeMutation_Mutation": "9450e06185f46531eca3e650c26fa8524f876924d1a8e9a3fb322305044bdac3",
  "AddPhoneNumber": "26ae865f0686a910a86759c069eb1c0085d78b55a8abf64444ec63b03c76fb58",
  "AnnotateWithIdsProviderQuery": "b4e6992c3af8f208ab2b3979dce48889835736ed29f623ea9f609265018d0d8f",
  "AvailableBotsListModalPaginationQuery": "3be373baa573ccd196b9d71c94953b1d1bc586625bd64efe51655d75e68bbfb7",
  "AvailableBotsSelectorModalPaginationQuery": "dd9281852c9a4d9d598f5a215e0143a8f76972c08e84053793567f7a76572593",
  "BotInfoFormRunCheckMutation": "87d55551061151b852fd7c53ec34dbb1ae784516b0ba2df5255b201f0d4e1444",
  "BotInfoModalQuery": "33254e9e91d63d16dbac1d70aa6accfb31786be05f7749772a32bc37d9ccb799",
  "BotLandingPageQuery": "fb2f3e506be25ff8ba658bf55cd2228dec374855b6758ec406f0d1274bf5588d",
  "BotSelectorModalQuery": "b1ed351177d82da55670039a971c647b87874d28c5e137b8eb9c9fdf7fb30f7b",
  "BotSwitcherModalQuery": "54023ee8b691543982b2819491532532c317b899918e049617928137c26d47f5",
  "ChatDeleteConfirmationModalQuery": "716c8cc3ac6c13d6b41ceb2404e3a28c63aea6d166bf071dca1f98e0377727c3",
  "ChatHelpersSendNewChatMessageMutation": "de5e755e5887f89b558abb7dbbe67cd459dd89f088957e4146253c29942576b0",
  "ChatHistoryFilteredListPaginationQuery": "47da1e74c53f6d0e0099389bd91b805b77c579807b926aa95d80d6721b6ac227",
  "ChatHistoryListPaginationQuery": "808e3f67fd13e64185607c0516277fe0ae48624c5b3b0e1a221d4ea72ecdaadb",
  "ChatHomeMainInputContainerOptimisticBotQuery": "1c9267ecff73cb27a8e7d94a3f5b5fe665a82abe0fdd61be2e54dd38c0e61639",
  "ChatHomeMainInputContainerOptimisticViewerQuery": "21f0eb43ab07d97d4a30bcf007db4797b95e852fb6537e8dbbc002da45ba4fac",
  "ChatListPaginationQuery": "dc3f4d34f13ed0a22b0dbfa6a1924a18922f7fe3a392b059b0c8c2134ce4ec8a",
  "ChatLoaderQuery": "d9467ac216e21b510eb8e72a2888289d173c9d5ce399b072fd88bee3da1b1459",
  "ChatPageBotBotsPagination": "ed9017f85fe2fedbf02b2d000cb4b551d2ec870715d0c7bce6d54a0f3f9b657b",
  "ChatPageQuery": "9f1a8daf09aa745bb1876d2999ba830e6bb28108da6dc34a8fc2c2554e650e44",
  "ChatsHistoryPageQuery": "050767d78f19014e99493016ab2b708b619c7c044eebd838347cf259f0f2aefb",
  "ChatSetTitle": "24574aab7fedf86d1654bbc70bf5421abbc33e195aa1c11178697023a27a912e",
  "ChatSettingsModalQuery": "41910ff112abaa713edd836cbb7fc567433f3f7ac3a61659fffca6306f7288ac",
  "ChatSubscriptionPaywallModalQuery": "559ac4c7c8f0f6f50148d255bb6318107034375df7bca4214f608cd65b573a21",
  "ChatSwitcherRefetchQuery": "815b8e6406bd19b25da36523b8b33c8c25e6db2fe93505117bb583c2d9dd60e4",
  "ChatTitleUpdated": "740e2c7ab27297b7a8acde39a400b932c71beb7e9b525280fc99c1639f1be93a",
  "ContinueChatFromPoeShare": "a220810c2d1d3b5284b6be44309a3d2b197c312a79b1a27f165a12f1508322bd",
  "ContinueChatIndexPageQuery": "a7eea6eebd14aa355723514558762315d0b4df46205b70f825d288d5ed1635ec",
  "ContinueChatPageQuery": "fe3a4d2006b1c4bb47ac6dea0639bc9128ad983cf37cbc0006c33efab372a19d",
  "CreateBotIndexPageQuery": "6bd24eb031dd0d427ddeef0c4113d9b3800aa44b62aed25143d6a95251765e38",
  "CreateBotPageQuery": "4fa5e0703c416fc6b40c5e2fcfcac66301ed0c8d32bafb5d69300e7553ef1f8f",
  "CreateChatMutation": "f1322c9c34d4140d420aeb9151cdeebc2235d381ada0037c845572310f613b7d",
  "CreateChatWithTitle": "6cf8cddd6594901bd4a7dc6ddeffc91485c21c817e8f7fa07fae9d71d9807d71",
  "CreateCheckoutSession": "5eb43e7c83974acc6680e1abe4c169296d0b346c42cc20d487762163402ea8e5",
  "CreateCustomerPortalSession": "4d43136f33aba6b6dea2ac8cd295e03bd841b7c99bf772940fa06a623a331786",
  "CreateMessagesToContinueChatMutation": "00b66f0117fab1ab6cdcf7e98819c1e3196736253b6a158316a49f587b964d25",
  "DeleteAccountMutation": "4e9651277464843d4d42fbfb5b4ccb1c348e3efe090d6971fa7a3c2cabc7ea5c",
  "DeleteChat": "5df4cb75c0c06e086b8949890b1871a9f8b9e431a930d5894d08ca86e9260a18",
  "DeleteMessageMutation": "8d1879c2e851ba163badb6065561183600fc1b9de99fc8b48b654eb65af92bed",
  "DeleteUserMessagesMutation": "3f60d527c3f636f308b3a26fc3a0012be34ea1a201e47a774b4513d8a1ba8912",
  "DismissDismissible": "b133084411c0a7a2353f6cfacd3d115260c34ddc5d97cf7f19a16e8cb4410803",
  "EditBotIndexPageQuery": "52c3db81cca5f44ae4de3705633488511bf7baa773c3fe2cb16b148f5b5cf55e",
  "EditBotPageQuery": "67c96902edcb66854106892671c816d9f7c3d8910f5a6b364f8b9f3c2bc7a37a",
  "EmailUnsubscribe": "eacf2ae89b7a30460619ccfb0d5a4e6007cfbcf0286ec7684c24192527a00263",
  "EmbedLoggedOutPageQuery": "e81580f4126215186e8a5d18bdedcf7c056b634d4d864f54b948765c8c21aef9",
  "ExploreBotsCarouselContainerQuery": "e46511b51cb2e9244225e1e6509c6a696dde271e45da74ce66853379eaeb80d6",
  "ExploreBotsCarouselLazyLoadedContainerQuery": "846522f24edbbad1331cedfe311ba0c8e365cf33aee1bb1e3f0e03156f1a0536",
  "ExploreBotsCarouselPagedContainerPaginationQuery": "619df00e336f6bbad2bbc2626aa74f97eb12efb50f403339cc780041aa9897e0",
  "ExploreBotsIndexPageQuery": "a302645924e901879b661c3656575ea31cfc23966902dc151675636afaf685b5",
  "ExploreBotsListPaginationQuery": "78f994251a3508ddbe702dca589d717a18f2032221a93fac208d7fba9d6ac5d2",
  "ExploreBotsPageQuery": "be8c7ca9725a477d6b04f907f3c0f0f58dd7647550555811720ffbac3c90ecfb",
  "ExploreBotsSidebarQuery": "00f42e3842c63cfcfcebad6402cdaa1df1c3fa7ffe3efbe0437a08a151eca87e",
  "GenerateAppleAuthNonceMutation": "c3e0c1b990cd17322716d0fa943a8ddc0ffecf45294ad013ccc883954c2171fc",
  "HandleBotChatEmbedPageQuery": "60a48e1b772e6830ddbdb54f19e837beef949d4fc146c51b1f50469f40b7650b",
  "HandleBotChatPageQuery": "dc1891a1d9b3ca42c773a69e9985f95e78a13ad5858cef0574c7f4ce87004a77",
  "HandleProfileIndexPageQuery": "0243e1784c33ae913d8a3ad20fc1252b930b6741ff9d78bd776e2df4f93f55ee",
  "HandleProfilePageQuery": "61b9722aa439c027110908b160db683f623e8affcde2d5f66378375b9ae668e3",
  "IntroMainQuery": "47f2c9bb41be5238968c81c82f2d2cff4100c73fcc70a9f592825bb40c0efc8d",
  "LayoutLeftSidebarQuery": "073fc8aad11bae987f5b70a68a0c2fedf8c8b3f2702757cdc68f8aedd1ee8103",
  "LayoutRightSidebarQuery": "ae7498e7255414c3c0bf07a4a8fd16bf880e73995d1046baf882c7119abe6f77",
  "LoginPageQuery": "538d23244211dfe6ed3228518508ebc728f9f8165950d5a19fc5467c2f0b9a1f",
  "LoginWithVerificationCodeMutation": "0d5aecd57239d518c25dc972569ee77dd9610a114610a6a3e87b87fdd8f1ba90",
  "LogoutAllSessionsMutation": "1e62b26302959ca753def8678e817b2c1ad94efdb21872dbf0f8bffcb892aed4",
  "LogoutMutation": "1d2e52b19e15a6aa0ec93d8e4a3a9653b9ceb4c1f365c7d9c4451d835505eef2",
  "MarkAndroidAppDownloadPromptSeen": "ed6891c8913983cc4fd0bfed9760e9738743419712ce6681841217ed0bb8c915",
  "MarkMultiplayerNuxCompleted": "c1b1f2ce72d9f8e9cd7bbe1eecbf6e3bed3366df6a18b179b07ddfd9f1f8b3b1",
  "MessageAdded": "6d5ff500e4390c7a4ee7eeed01cfa317f326c781decb8523223dd2e7f33d3698",
  "ChatHelpers_messageCancel_Mutation": "59b10f19930cf95d3120612e72d271e3346a7fc9599e47183a593a05b68c617e",
  "MessageCancelled": "dfcedd9e0304629c22929725ff6544e1cb32c8f20b0c3fd54d966103ccbcf9d3",
  "MessageDeleted": "91f1ea046d2f3e21dabb3131898ec3c597cb879aa270ad780e8fdd687cde02a3",
  "MessageLimitUpdated": "d862b8febb4c058d8ad513a7c118952ad9095c4ec0a5471540133fc0a9bd3797",
  "MessageUnvoteMutation": "af2b91f09ab2ccf53ba9176a86b9934b98a865adf228b2ac3a548d6397f382f3",
  "MessageVoteMutation": "199fd8402c70ac10c5b05ba31587a0beff3acc39c7194362610ad50bf20299ed",
  "NewLandingPageQuery": "f36fbfcbad84b02876a254ba77ecf78f96360e77291766209b9e7655852440da",
  "NumTokensFromPromptQuery": "1d9bef79811f3b2ddca5ce4027b7eaa31a51bbeed1edf8b6f72e2e0d09d80609",
  "NuxInitialModalQuery": "f8cd0d8494afe3b5dbb349baa28d3ac21f2219ce699e2d59a2345c864905e0c3",
  "NuxInitialModal_poeSetHandle_Mutation": "93a0c939986bb344f87a76d9d709f147a23f1a45ec26e291bcea9acf66b3215f",
  "OnboardingFreeTrialModalQuery": "d2cc659e3def4561ca15b268a97588c5af6cd154afb001312aa69f63c5b2cc9e",
  "OnboardingPaywallModalQuery": "b413e41e89125528f1b2e7f472bde37f6f48a25cb774f4ea3ff883644c973cca",
  "OnboardingPaywallWithGraphicModalQuery": "f986cd3dc4fbab98927983c5d4ed78fa095af78392cf3880af9203dea975890d",
  "OptimisticChatLoaderQuery": "8633378bbe67e397457bebb256d7dc0c48f9a973315f3158cfb2f4fc08ad6c06",
  "PageBlockerQuery": "d1ab792fce4d3f91777b49856d44b2d9cbb6ad1231e1116c407a0208604181e1",
  "PageWrapperQuery": "fa2f44e7aafe6d1698f88ef7443fe13727765570ab504555a15d9c1578ded275",
  "PagesBotNameQuery": "a156136af92b189768540f864445f0b8d9191584530def6b1a5502c843539cfb",
  "PagesDefaultBotChatPageQuery": "75bd0877369c2b4191c936572822ce1875c980f1f6f8683381bd4a6850bdea92",
  "BotInfoCardActionBar_poeBotDelete_Mutation": "ddda605feb83223640499942fac70c440d6767d48d8ff1a26543f37c9bb89c68",
  "BotInfoCardActionBar_poeRemoveBotFromUserList_Mutation": "94f91aa5973c4eb74b9565a2695e422a2ff2afd334c7979fe6da655f4a430d85",
  "PoeBotCreate": "fcc424e9f56e141a2f6386b00ea102be2c83f71121bd3f4aead1131659413290",
  "PoeBotDelete": "c5e5ee2fdac007b02d074ce7882a0631bfbccc73d8833ba8765297c5ea782bb6",
  "PoeBotEdit": "eb93047f1b631df35bd446e0e03555fcc61c8ad83d54047770cd4c2c418f8187",
  "PoeBotFollow": "efa3f25f6cd67f9dea757be50305c0caa6a4e51f52ffba7e4a1c1f2c84d6dbd0",
  "PoeBotUnfollow": "db2281f3efa305db62d38964b640e982076491c2c59d5be3303feae343fe8914",
  "PoeRemoveBotFromUserList": "89e756b668b2318fa73c2a9dde4608a4529c74844667417c0cfb245e7e04e96e",
  "PoeSetBio": "66fb99ec59fa17bc4487f944d116bc920161faced58a3ce99e82cb61af61468e",
  "PoeSetHandle": "4139b28c6a152e2d074944a7cf7f133b453080c1660c4960e14418be363897bb",
  "PoeSetName": "c406a46fe6ff244ab2d665ea953fc8655d6816f1731505d830863d9b9c5021bf",
  "PoeSetProfilePhoto": "13106f2433e5d48a53e6804b76022e80c0fc9bf018eb5b5404d9e0a4acd94f1f",
  "PoeUserSetFollow": "dcc26e4e36b47af8af6bd0296ff85dfa8fc77a9c374ea5989afd0bf39ae4d35e",
  "PostIdPostPageQuery": "653c4768688ce6c8c14ca359ce536646b3de71a7e953c16381136399791c95a0",
  "ProfileIndexPageQuery": "4044ca7eb203e613f19dc76a4a05ca1df25bfdb2ff761a9d6dced6b0d61f219a",
  "ProfilePageQuery": "9505daf59f885463e5bd3bb2a1a9fc088e8634fbc7d5a0682f2ece11ee7548dd",
  "RemoveEmailMutation": "63750a7e41cc0ad3f6da0be1fdae9c243f1afab83cf44bb5c3df14243074681d",
  "RemoveUserPhoneNumberMutation": "7dadad6ac75a8a4e5c54479524c7821e748c043242476958262bb39fa60ccddb",
  "SaveContinueChatInfoMutation": "ae56678376401ae45dbba61aa6b1a55564877edc33605db6283e1dc3bdb0c8ff",
  "SearchResultsListPaginationQuery": "8466d0d19866f27eabef0657dc9a1822ed5260c44dc839d32cd9c329fe444e31",
  "SearchResultsMainQuery": "f8197cc6f654594d98c414e9cb6915d3004be06b15e1c20994c88bc882289211",
  "SelectorTestPageQuery": "9ec86fe8e3d0d3b264d0fab0feb73e38c86d616c7c3d8340d7a6146bd8445ed3",
  "SendMessageMutation": "f7887d68040b45a71d92c46b067fd88539d5d4a51dd9102bde3a4f4fe109bc56",
  "SendVerificationCodeMutation": "d418fa3d2357d089b20065226041180573fa0b0382914a90cf905435281af520",
  "SetPrimaryEmailMutation": "01e75a6d937351b304ca9cc0b231e43587a5923e7f8618863bdf996df38d28b5",
  "SettingsDefaultBotSectionMutation": "4084604e8741af8650ac6b4236cdfa13c91a70cf1c63ad8a368706a386d0887e",
  "SettingsIndexPageQuery": "c9cab56d7329fc2665760ceeb92005e2b3449351a5fb24d906e52587ca87ca64",
  "SettingsPageQuery": "1633485f58c7f2e730a34446b8566c40b5fe2a75ad82b930e3374d8c222b5983",
  "ShareCodeSharePageQuery": "e56f5cb9c7fc9872d053ddaef3dd7827067530b014f59e3ed07bc5e21a0f4334",
  "ShareMessageMutation": "2491190f42c1f5265d8dbaaaf7220dbfa094044fdfb2429fd7f2e35f863bc5e1",
  "ContinueChatCTAButton_continueChatFromPoeShare_Mutation": "8b7bbb788463708e87ea979a383ddf6cbbb8818305add8b30c275a13ce9c7a95",
  "SignupOrLoginWithAppleMutation": "649943f9929600796b30f48a47094af56a5d86b4556e34e91aa8ea834cda5fda",
  "SignupOrLoginWithGoogleMutation": "519c2241faeb2bade473ed190913365604eee13ca97b67775b2c7b1aad0fb095",
  "SignupOrLoginWithQuoraMutation": "ee2498e8837e7b975806613401f5aa4ba18d03fdcc9fde0c59efc75717103df5",
  "SignupWallModalInnerQuery": "56f7718c8e586c16065f7b57dcbcf61d3789ab937590e8e77d458613b3c8f325",
  "SignupWithVerificationCodeMutation": "6a9b90b76ee9c058f55a3d659c093a5eca6a5ddbef233dbecee389501b1e5dbf",
  "StaticContentQuery": "15267bf130fbe298a6f60334f57ccf62bc16ff06c74d5778ba54b4b4f21f8d0c",
  "SubscriptionTosQuery": "6696950c5612023d877acd6a6f9026668960994825d3fa71a80528c316510c2f",
  "SubscriptionsMutation": "5a7bfc9ce3b4e456cd05a537cfa27096f08417593b8d9b53f57587f3b7b63e99",
  "UniversalLinkPageQuery": "ec7c629dd6ec79f9d26dda9c4ef9cb1e24aa41d7b92090596b6639eeee5e6cc8",
  "UpdatePhoneNumber": "c49f5f64947c2946f8007f366bbc0ca5b1f0bbbdc6b72ad97be90533f0e83c28",
  "UseBotSelectorBotQuery": "6af7249e90de59baef2e770f7e773f9f7730fd49db6b4e82035c49a078818534",
  "UseBotSelectorViewerBotsPaginationQuery": "e7dbf27efba69f014750ee56ac13f21262e76e161c6e58d435ae75935798d1b0",
  "UseStopMessageAndSendChatBreak": "9b95c61cd6cb41230a51fb360896454dde1ae6d1edb6f075504cb83a52422bc9",
  "UserEditBioModalQuery": "b78089f19d1071ad9440d5a2696588b0e82a012f6b40dca68f071cc0a49727f2",
  "UserEditHandleModalQuery": "ecee1f772c401f6e429ba7ebe088eedc0aa6d24dfa4cae0ec6f54bb3c5a5c653",
  "UserEditNameModalQuery": "dd72d69698a46097386b73b19677a84b6bcba51b3df3790e67d804b6da686787",
  "UserEditProfilePicModalQuery": "7f69ff6407a1360570863b09a9c02bf0a4bdbd8de2b04e5dde4eec031a6f62e5",
  "UserFolloweesListModalQuery": "b219f7e8b7c8d21aaa0979d44bfc3935501719e3fe18cbe86b459eced5f290d2",
  "UserFollowersListModalQuery": "86b007fa15b2de6f7eb527050832d342dde837aaedfb61bfdd1bf1201b860b61",
  "UserProfileConfigurePreviewModalQuery": "abec61f90eebcc3b914487db0ba35ff6ec53c1f7c29f40f59222cee5b8832a52",
  "ViewerStateUpdated": "ee640951b5670b559d00b6928e20e4ac29e33d225237f5bdfcb043155f16ef54",
  "WebSpeedUpsellQuery": "d8556da659d21dc2c583248c1c617ca20492b64c6948ae4a16256c0848f9c32e",
  "WebSubscriptionAnnouncementQuery": "a1b332d7d6816accfccb619e0f0728771ac7c398881fa423051d06551cd0f069",
  "WebSubscriptionPaywallModalQuery": "4d248f3aa4fbf68eb57a1bdda52a6dc5f38dd3b1234c01a95d4b17fdfbd922db",
  "WebSubscriptionPaywallWrapperQuery": "f84fada22609f5dc5933e7ef1e54001fa5e76871836f268e68ad8df7e202f6ca",
}

def generate_payload(query_name, variables) -> str:
    if query_name == "recv":
        return generate_recv_payload(variables)
    payload = {
        "queryName": query_name,
        "variables": variables,
        "extensions": {
            "hash": QUERIES[query_name]
        }
    }
    return json.dumps(payload, separators=(",", ":"))

def generate_recv_payload(variables):
    payload = [
    {
      "category": "poe/bot_response_speed",
      "data": variables,
    }
    ]

    if random.random() > 0.9:
        payload.append({
        "category": "poe/statsd_event",
        "data": {
            "key": "poe.speed.web_vitals.INP",
            "value": random.randint(100, 125),
            "category": "time",
            "path": "/[handle]",
            "extra_data": {},
        },
        })
    return json.dumps(payload, separators=(",", ":"))

BOTS_LIST = {
    'Assistant': 'capybara',
    'Claude-instant-100k': 'a2_100k',
    'Claude-2-100k': 'a2_2',
    'Claude-instant': 'a2',
    'ChatGPT': 'chinchilla',
    'GPT-3.5-Turbo-Instruct': 'chinchilla_instruct',
    'ChatGPT-16k': 'agouti',
    'GPT-4': 'beaver',
    'GPT-4-32k': 'vizcacha',
    'Google-PaLM': 'acouchy',
    'Llama-2-7b': 'llama_2_7b_chat',
    'Llama-2-13b': 'llama_2_13b_chat',
    'Llama-2-70b': 'llama_2_70b_chat',
    'Code-Llama-7b': 'code_llama_7b_instruct',
    'Code-Llama-13b': 'code_llama_13b_instruct',
    'Code-Llama-34b': 'code_llama_34b_instruct',
    'Solar-0-70b':'upstage_solar_0_70b_16bit'
}

EXTENSIONS = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.txt': 'text/plain',
    '.py': 'text/x-python',
    '.js': 'text/javascript',
    '.ts': 'text/plain',
    '.html': 'text/html',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.c' : 'text/plain',
    '.cs': 'text/plain',
    '.cpp': 'text/plain',
}

def bot_map(bot):
    if bot in BOTS_LIST:
        return BOTS_LIST[bot]
    return bot.lower().replace(' ', '')
    
def generate_nonce(length:int=16):
      return "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def generate_file(file_path: list, proxy: dict=None):
    files = []   
    file_size = 0
    for file in file_path: 
        if is_valid_url(file):  
            file_name = file.split('/')[-1]
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in EXTENSIONS:
                content_type = EXTENSIONS[file_extension]
            else:
                raise RuntimeError("This file type is not supported. Please try again with a different file.") 
            with Client(timeout=20, proxies=proxy) as fetcher:
                response = fetcher.get(file)
                file_data = response.read()
            file_size += len(file_data)
        else: 
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in EXTENSIONS:
                content_type = EXTENSIONS[file_extension]
            else:
                raise RuntimeError("This file type is not supported. Please try again with a different file.") 
            file_name = os.path.basename(file)
            file_data = open(file, 'rb')
            file_size += os.path.getsize(file)
        files.append((file_name, file_data, content_type))
    return files, file_size

class PoeApi:
    BASE_URL = 'https://www.quora.com'
    HEADERS = {
        'Host': 'www.quora.com',
        'Accept': '*/*',
        'apollographql-client-version': '1.1.6-65',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Poe 1.1.6 rv:65 env:prod (iPhone14,2; iOS 16.2; en_US)',
        'apollographql-client-name': 'com.quora.app.Experts-apollo-ios',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }
    FORMKEY_PATTERN = r'formkey": "(.*?)"'

    def __init__(self, cookie: str, proxy: bool=False):
        self.cookie = cookie
        self.formkey = None
        if proxy == True:
            self.proxy = {"http://": f"http://127.0.0.1:10810",
                          "https://": f"http://127.0.0.1:10810"}
            self.client = Client(headers=self.HEADERS, timeout=180, proxies=self.proxy)
        else:
            self.proxy = None
            self.client = Client(headers=self.HEADERS, timeout=180)
        self.client.cookies.set('m-b', self.cookie)
        
        self.get_channel_settings()
        
        self.client.headers.update({
            'Quora-Formkey': self.formkey,
        })
        
        self.ws_connecting = False
        self.ws_connected = False
        self.ws_error = False
        self.active_messages = {}
        self.message_queues = {}
        self.current_thread = {}
        self.retry_attempts = 3
        self.message_generating = True
        self.ws_refresh = 3
        
        self.connect_ws()
        
    def __del__(self):
        self.client.close()

    def send_request(self, path: str, query_name: str="", variables: dict={}, file_form: list=[]):
        payload = generate_payload(query_name, variables)
        if file_form == []:
            headers= {'Content-Type': 'application/x-www-form-urlencoded'}
        else:
            fields = {'queryInfo': payload}
            for i in range(len(file_form)):
                fields[f'file{i}'] = file_form[i]
            payload = MultipartEncoder(
                fields=fields
                )
            headers = {'Content-Type': payload.content_type}
            payload = payload.to_string()
        response = self.client.post(f'{self.BASE_URL}/poe_api/{path}', data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"An unknown error occurred. Raw response data: {response.text}")
    
    def get_channel_settings(self):
        response_json = self.client.get(f'{self.BASE_URL}/poe_api/settings', headers=self.HEADERS, follow_redirects=True).json()
        self.ws_domain = f"tch{random.randint(1, int(1e6))}"[:9]
        self.formkey = response_json["formkey"]
        self.tchannel_data = response_json["tchannelData"]
        self.client.headers["Quora-Tchannel"] = self.tchannel_data["channel"]
        self.channel_url = f'wss://{self.ws_domain}.tch.{self.tchannel_data["baseHost"]}/up/{self.tchannel_data["boxName"]}/updates?min_seq={self.tchannel_data["minSeq"]}&channel={self.tchannel_data["channel"]}&hash={self.tchannel_data["channelHash"]}'
        print(self.channel_url)
        return self.channel_url
    
    def subscribe(self):
        response_json = self.send_request('gql_POST', "SubscriptionsMutation",
            {
                "subscriptions": [
                    {
                        "subscriptionName": "messageAdded",
                        "query": None,
                        "queryHash": "6d5ff500e4390c7a4ee7eeed01cfa317f326c781decb8523223dd2e7f33d3698",
                    },
                    {
                        "subscriptionName": "messageCancelled",
                        "query": None,
                        "queryHash": "dfcedd9e0304629c22929725ff6544e1cb32c8f20b0c3fd54d966103ccbcf9d3",
                    },
                    {
                        "subscriptionName": "messageDeleted",
                        "query": None,
                        "queryHash": "91f1ea046d2f3e21dabb3131898ec3c597cb879aa270ad780e8fdd687cde02a3",
                    },
                    {
                        "subscriptionName": "viewerStateUpdated",
                        "query": None,
                        "queryHash": "ee640951b5670b559d00b6928e20e4ac29e33d225237f5bdfcb043155f16ef54",
                    },
                    {
                        "subscriptionName": "messageLimitUpdated",
                        "query": None,
                        "queryHash": "d862b8febb4c058d8ad513a7c118952ad9095c4ec0a5471540133fc0a9bd3797",
                    },
                    {
                        "subscriptionName": "chatTitleUpdated",
                        "query": None,
                        "queryHash": "740e2c7ab27297b7a8acde39a400b932c71beb7e9b525280fc99c1639f1be93a",
                    },
                ]
            },
        )
        if response_json['data'] == None and response_json["errors"]:
            raise RuntimeError(f'Failed to subscribe by sending SubscriptionsMutation. Raw response data: {response_json}')
            
    def ws_run_thread(self):
        if not self.ws.sock:
            kwargs = {
                'http_proxy_host':"127.0.0.1",
                'http_proxy_port':10810,
                'proxy_type':'http'
            }
            self.ws.run_forever(**kwargs)
             
    def connect_ws(self, timeout=20):
        if self.ws_connected:
            return

        if self.ws_connecting:
            while not self.ws_connected:
                sleep(0.01)
            return

        self.ws_connecting = True
        self.ws_connected = False
        self.ws_refresh = 3
        
        while True:
            self.ws_refresh -= 1
            if self.ws_refresh == 0:
                self.ws_refresh = 3
                raise RuntimeError("Rate limit exceeded for sending requests to poe.com. Please try again later.")
            self.get_channel_settings()
            try:
                self.subscribe()
                break
            except:
                sleep(1)
                continue

        self.ws = websocket.WebSocketApp(self.channel_url, 
                                         on_message=lambda ws, msg: self.on_message(ws, msg), 
                                         on_open=lambda ws: self.on_ws_connect(ws), 
                                         on_error=lambda ws, error: self.on_ws_error(ws, error), 
                                         on_close=lambda ws, close_status_code,close_message: self.on_ws_close(ws, close_status_code, close_message)
                                         )

        t = threading.Thread(target=self.ws_run_thread, daemon=True)
        t.start()

        timer = 0
        while not self.ws_connected:
            sleep(0.01)
            timer += 0.01
            if timer > timeout:
                self.ws_connecting = False
                self.ws_connected = False
                self.ws_error = True
                self.ws.close()
                raise RuntimeError("Timed out waiting for websocket to connect.")

    def disconnect_ws(self):
        self.ws_connecting = False
        self.ws_connected = False
        if self.ws:
            self.ws.close()

    def on_ws_connect(self, ws):
        self.ws_connecting = False
        self.ws_connected = True

    def on_ws_close(self, ws, close_status_code, close_message):
        self.ws_connecting = False
        self.ws_connected = False
        if self.ws_error:
            logger.warning("Connection to remote host was lost. Reconnecting...")
            self.ws_error = False
            self.connect_ws()

    def on_ws_error(self, ws, error):
        logger.warning(error)
        self.ws_connecting = False
        self.ws_connected = False
        self.ws_error = True

    def on_message(self, ws, msg):
        try:
            data = json.loads(msg)
            if not "messages" in data:
                return
            for message_str in data["messages"]:
                message_data = json.loads(message_str)
                if message_data["message_type"] != "subscriptionUpdate" or message_data["payload"]["subscription_name"] != "messageAdded":
                    continue
                message = message_data["payload"]["data"]["messageAdded"]
        
                copied_dict = self.active_messages.copy()
                for key, value in copied_dict.items():
                    if value == message["messageId"] and key in self.message_queues:
                        self.message_queues[key].put(message)
                        return

                    elif key != "pending" and value == None and message["state"] != "complete":
                        self.active_messages[key] = message["messageId"]
                        self.message_queues[key].put(message)
                        return
        except Exception:
            logger.exception(f"Failed to parse message: {msg}")
            self.disconnect_ws()
            self.connect_ws()
    
    def get_available_bots(self, count: int=25, get_all: bool=False):
        self.bots = {}
        if not (get_all or count):
            raise TypeError("Please provide at least one of the following parameters: get_all=<bool>, count=<int>")
        response = self.send_request('gql_POST',"AvailableBotsSelectorModalPaginationQuery", {}) 
        bots = [
            each["node"]
            for each in response["data"]["viewer"]["availableBotsConnection"]["edges"]
            if each["node"]["deletionState"] == "not_deleted"
        ]
        cursor = response["data"]["viewer"]["availableBotsConnection"]["pageInfo"]["endCursor"]
        if len(bots) >= count and not get_all:
            self.bots.update({bot["handle"]: {"bot": bot} for bot in bots})
            return self.bots
        while len(bots) < count or get_all:
            response = self.send_request("gql_POST", "AvailableBotsSelectorModalPaginationQuery", {"cursor": cursor})
            new_bots = [
                each["node"]
                for each in response["data"]["viewer"]["availableBotsConnection"]["edges"]
                if each["node"]["deletionState"] == "not_deleted"
            ]
            cursor = response["data"]["viewer"]["availableBotsConnection"]["pageInfo"]["endCursor"]
            bots += new_bots
            if len(new_bots) == 0:
                if not get_all:
                    logger.warning(f"Only {len(bots)} bots found on this account")
                else:
                    logger.info(f"Total {len(bots)} bots found on this account")
                self.bots.update({bot["handle"]: {"bot": bot} for bot in bots})
                return self.bots
            
        logger.info("Succeed to get available bots")
        self.bots.update({bot["handle"]: {"bot": bot} for bot in bots})
        return self.bots
    
    def get_chat_history(self, bot: str=None, count: int=None, interval: int=50, cursor: str=None):

        chat_bots = {'data': {}, 'cursor': None}
        
        if count != None:
            interval = count
        
        if bot == None:
            response_json = self.send_request('gql_POST', 'ChatHistoryListPaginationQuery', {'count': interval, 'cursor': cursor})
            if response_json['data']['chats']['pageInfo']['hasNextPage']:
                cursor = response_json['data']['chats']['pageInfo']['endCursor']
                chat_bots['cursor'] = cursor  
            else:
                chat_bots['cursor'] = None
            edges = response_json['data']['chats']['edges']
            # print('-'*38+' \033[38;5;121mChat History\033[0m '+'-'*38)
            # print('\033[38;5;121mChat ID\033[0m  |     \033[38;5;121mChat Code\033[0m       |           \033[38;5;121mBot Name\033[0m            |       \033[38;5;121mChat Title\033[0m')
            # print('-' * 90)
            for edge in edges:
                chat = edge['node']
                model = bot_map(chat["defaultBotObject"]["displayName"])
                # print(f'{chat["chatId"]} | {chat["chatCode"]} | {model}' + (30-len(model))*' ' + f'| {chat["title"]}')
                if model in chat_bots['data']:
                    chat_bots['data'][model].append({"chatId": chat["chatId"],"chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]})
                else:
                    chat_bots['data'][model] = [{"chatId": chat["chatId"], "chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]}]
            # Fetch more chats
            if count == None:
                while response_json['data']['chats']['pageInfo']['hasNextPage']:
                    response_json = self.send_request('gql_POST', 'ChatHistoryListPaginationQuery', {'count': interval, 'cursor': cursor})
                    edges = response_json['data']['chats']['edges']
                    for edge in edges:
                        chat = edge['node']
                        model = bot_map(chat["defaultBotObject"]["displayName"])
                        # print(f'{chat["chatId"]} | {chat["chatCode"]} | {model}' + (30-len(model))*' ' + f'| {chat["title"]}')
                        if model in chat_bots['data']:
                            chat_bots['data'][model].append({"chatId": chat["chatId"],"chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]})
                        else:
                            chat_bots['data'][model] = [{"chatId": chat["chatId"], "chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]}]    
                    cursor = response_json['data']['chats']['pageInfo']['endCursor']  
                    chat_bots['cursor'] = cursor      
                if not response_json['data']['chats']['pageInfo']['hasNextPage']:
                    chat_bots['cursor'] = None  
                # print('-' * 90)  
        else:
            model = bot.lower().replace(' ', '')
            handle = model
            for key, value in BOTS_LIST.items():
                if model == value:
                    handle = key
                    break
            response_json = self.send_request('gql_POST', 'ChatHistoryFilteredListPaginationQuery', {'count': interval, 'handle': handle, 'cursor': cursor})
            if response_json['data'] == None and response_json["errors"]:
                raise ValueError(
                    f"Bot {bot} not found. Make sure the bot exists before creating new chat."
                )
            if response_json['data']['filteredChats']['pageInfo']['hasNextPage']:
                cursor = response_json['data']['filteredChats']['pageInfo']['endCursor']
                chat_bots['cursor'] = cursor  
            else:
                chat_bots['cursor'] = None
            edges = response_json['data']['filteredChats']['edges']
            for edge in edges:
                chat = edge['node']
                try:
                    if model in chat_bots['data']:
                        chat_bots['data'][model].append({"chatId": chat["chatId"],"chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]})
                    else:
                        chat_bots['data'][model] = [{"chatId": chat["chatId"], "chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]}]
                except:
                    pass 
            # Fetch more chats
            if count == None:
                while response_json['data']['filteredChats']['pageInfo']['hasNextPage']:
                    response_json = self.send_request('gql_POST', 'ChatHistoryFilteredListPaginationQuery', {'count': interval, 'handle': handle, 'cursor': cursor})
                    edges = response_json['data']['filteredChats']['edges']
                    for edge in edges:
                        chat = edge['node']
                        try:
                            if model in chat_bots['data']:
                                chat_bots['data'][model].append({"chatId": chat["chatId"],"chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]})
                            else:
                                chat_bots['data'][model] = [{"chatId": chat["chatId"], "chatCode": chat["chatCode"], "id": chat["id"], "title": chat["title"]}]
                        except:
                            pass      
                    cursor = response_json['data']['filteredChats']['pageInfo']['endCursor']  
                    chat_bots['cursor'] = cursor  
                if not response_json['data']['filteredChats']['pageInfo']['hasNextPage']:
                    chat_bots['cursor'] = None
        return chat_bots
    
    def get_threadData(self, bot: str="", chatCode: str=None, chatId: int=None):
        id = None
        title = None
        if bot not in self.current_thread:
            self.current_thread[bot] = self.get_chat_history(bot=bot)['data'][bot]
        elif len(self.current_thread[bot]) <= 1:
            self.current_thread[bot] = self.get_chat_history(bot=bot)['data'][bot]
        if chatCode != None:
            for chat in self.current_thread[bot]:
                if chat['chatCode'] == chatCode:
                    chatId = chat['chatId']
                    id = chat['id']
                    title = chat['title']
                    break
        elif chatId != None:
            for chat in self.current_thread[bot]:
                if chat['chatId'] == chatId:
                    chatCode = chat['chatCode']
                    id = chat['id']
                    title = chat['title']
                    break
        return {'chatCode': chatCode, 'chatId': chatId, 'id': id, 'title': title}
                
    def retry_request(self, chatCode, apiPath, variables, file_form):
        while self.ws_error:
            sleep(0.01)
        self.connect_ws()
        message_ids = []
        variablesData = {'chatCode': chatCode}
        response_json = self.send_request('gql_POST', 'ChatPageQuery', variablesData)
        edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
        edges.reverse()
        for edge in range(len(edges)):
            if edge < (len(edges)-1):
                if edges[edge]['node']['state'] == 'error':
                    message_ids.append(edges[edge]['node']['messageId'])
                    if edges[edge+1]['node']['author'] == 'human' and edges[edge+1]['node']['state'] == 'complete':
                        message_ids.append(edges[edge+1]['node']['messageId'])
        self.delete_message(message_ids)
        logger.info(f'Deleted {len(message_ids)} error messages')
        sleep(2)
        logger.info('Resending message...')
        response_json = self.send_request(apiPath, 'SendMessageMutation', variables, file_form)
        if response_json['data'] == None and response_json["errors"]:
            raise RuntimeError(f"An unknown error occurred. Raw response data: {response_json}")
        else:
            if response_json['data']['messageEdgeCreate']['status'] == 'reached_limit':
                    raise RuntimeError(f"Daily limit reached for {variables['bot']}.")
            try:
                human_message = response_json["data"]["messageEdgeCreate"]["message"]
                human_message_id = human_message["node"]["messageId"]
            except TypeError:
                raise RuntimeError(f"An unknown error occurred. Raw response data: {response_json}")
            self.message_generating = True
            self.active_messages[human_message_id] = None
            self.message_queues[human_message_id] = queue.Queue()
            return human_message_id

    def send_message(self, bot: str, message: str, chatId: int=None, chatCode: str=None, file_path: list=[], suggest_replies: bool=False, timeout: int=10) -> dict:
        bot = bot_map(bot)
        self.retry_attempts = 3
        timer = 0
        while None in self.active_messages.values():
            sleep(0.01)
            timer += 0.01
            if timer > timeout:
                raise RuntimeError("Timed out waiting for other messages to send.")
        self.active_messages["pending"] = None
        
        while self.ws_error:
            sleep(0.01)
        self.connect_ws()
        
        attachments = []
        if file_path == []:
            apiPath = 'gql_POST'
            file_form = []
        else:
            apiPath = 'gql_upload_POST'
            file_form, file_size = generate_file(file_path, self.proxy)
            if file_size > 100000000:
                raise RuntimeError("File size too large. Please try again with a smaller file.")
            for i in range(len(file_form)):
                attachments.append(f'file{i}')
        
        if (chatId == None and chatCode == None):
            try:
                variables = {"chatId": None, "bot": bot,"query":message, "shouldFetchChat": True, "source":{"sourceType":"chat_input","chatInputMetadata":{"useVoiceRecord":False,}}, "clientNonce": generate_nonce(),"sdid":"","attachments":attachments}
                message_data = self.send_request(apiPath, 'SendMessageMutation', variables, file_form)
        
                if message_data["data"] == None and message_data["errors"]:
                    raise ValueError(
                        f"Bot {bot} not found. Make sure the bot exists before creating new chat."
                    )
                else:
                    status = message_data['data']['messageEdgeCreate']['status']
                    if status == 'success' and file_path != []:
                        for file in file_form:
                            logger.info(f"File {file[0]} uploaded successfully")
                    elif status == 'unsupported_file_type' and file_path != []:
                        logger.warning("This file type is not supported. Please try again with a different file.")
                    elif status == 'reached_limit':
                        raise RuntimeError(f"Daily limit reached for {bot}.")
                    elif status == 'too_many_tokens':
                        raise RuntimeError(f"{message_data['data']['messageEdgeCreate']['statusMessage']}")
                        
                    logger.info(f"New Thread created | {message_data['data']['messageEdgeCreate']['chat']['chatCode']}")
                
                message_data = message_data['data']['messageEdgeCreate']['chat']
                chatCode = message_data['chatCode']
                chatId = message_data['chatId']
                title = message_data['title']
                if bot not in self.current_thread:
                    self.current_thread[bot] = [{'chatId': chatId, 'chatCode': chatCode, 'id': message_data['id'], 'title': message_data['title']}]
                elif self.current_thread[bot] == []:
                    self.current_thread[bot] = [{'chatId': chatId, 'chatCode': chatCode, 'id': message_data['id'], 'title': message_data['title']}]
                else:
                    self.current_thread[bot].append({'chatId': chatId, 'chatCode': chatCode, 'id': message_data['id'], 'title': message_data['title']})
                del self.active_messages["pending"]
            except Exception as e:
                del self.active_messages["pending"]
                raise e
            try:
                human_message = message_data['messagesConnection']['edges'][0]['node']['text']
                human_message_id = message_data['messagesConnection']['edges'][0]['node']['messageId']
            except TypeError:
                raise RuntimeError(f"An unknown error occurred. Raw response data: {message_data}")
        else:
            chatdata = self.get_threadData(bot, chatCode, chatId)
            chatCode = chatdata['chatCode']
            chatId = chatdata['chatId']
            title = chatdata['title']
            variables = {'bot': bot, 'chatId': chatId, 'query': message, 'shouldFetchChat': False, 'source': { "sourceType": "chat_input", "chatInputMetadata": {"useVoiceRecord": False}}, "clientNonce": generate_nonce(), 'sdid':"", 'attachments': attachments}
            
            try:
                message_data = self.send_request(apiPath, 'SendMessageMutation', variables, file_form)
                if message_data["data"] == None and message_data["errors"]:
                    raise RuntimeError(f"An unknown error occurred. Raw response data: {message_data}")
                else:
                    status = message_data['data']['messageEdgeCreate']['status']
                    if status == 'success' and file_path != []:
                        for file in file_form:
                            logger.info(f"File {file[0]} uploaded successfully")
                    elif status == 'unsupported_file_type' and file_path != []:
                        logger.warning("This file type is not supported. Please try again with a different file.")
                    elif status == 'reached_limit':
                        raise RuntimeError(f"Daily limit reached for {bot}.")
                    elif status == 'too_many_tokens':
                        raise RuntimeError(f"{message_data['data']['messageEdgeCreate']['statusMessage']}")
                del self.active_messages["pending"]
            except Exception as e:
                del self.active_messages["pending"]
                raise e
                    
            try:
                human_message = message_data["data"]["messageEdgeCreate"]["message"]
                human_message_id = human_message["node"]["messageId"]
            except TypeError:
                raise RuntimeError(f"An unknown error occurred. Raw response data: {message_data}")
        
        self.message_generating = True
        self.active_messages[human_message_id] = None
        self.message_queues[human_message_id] = queue.Queue()

        last_text = ""
        message_id = None
        
        while True:
            try:
                message = self.message_queues[human_message_id].get(timeout=timeout)
            except queue.Empty:
                del self.active_messages[human_message_id]
                del self.message_queues[human_message_id]
                try:
                    if self.retry_attempts > 0:
                        self.retry_attempts -= 1
                        logger.warning(f"Retrying request {3-self.retry_attempts}/3 times...")
                    else:
                        self.retry_attempts = 3
                        raise RuntimeError("Timed out waiting for response.")
                    human_message_id = self.retry_request(chatCode, apiPath, variables, file_form)
                    continue
                except Exception as e:
                    raise e
            
            message["chatCode"] = chatCode
            message["chatId"] = chatId
            message["title"] = title

            if message["state"] == "error_user_message_too_long":
                message["response"]  = 'Message too long. Please try again!'
                yield message
                break
            
            message["response"] = message["text"][len(last_text):]
            
            yield message
            
            if message["state"] == "complete" or not self.message_generating:
                if last_text and message["messageId"] == message_id:
                    break
                else:
                    continue
            
            last_text = message["text"]
            message_id = message["messageId"]
            
        def recv_post_thread():
            bot_message_id = self.active_messages[human_message_id]
            sleep(2.5)
            self.send_request("receive_POST", "recv", {
                "bot_name": bot,
                "time_to_first_typing_indicator": 300, # randomly select
                "time_to_first_subscription_response": 600,
                "time_to_full_bot_response": 1100,
                "full_response_length": len(last_text) + 1,
                "full_response_word_count": len(last_text.split(" ")) + 1,
                "human_message_id": human_message_id,
                "bot_message_id": bot_message_id,
                "chat_id": chatId,
                "bot_response_status": "success",
            })
            sleep(0.5)
            
        def get_suggestions(queue, chatCode: str=None, timeout: int=5):
            variables = {'chatCode': chatCode}
            state = 'incomplete'
            suggestions = []
            start_time = time()
            while True:
                elapsed_time = time() - start_time
                if elapsed_time >= timeout:
                    break
                sleep(0.5)
                response_json = self.send_request('gql_POST', 'ChatPageQuery', variables)
                hasSuggestedReplies = response_json['data']['chatOfCode']['defaultBotObject']['hasSuggestedReplies']
                edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
                if hasSuggestedReplies and edges:
                    latest_message = edges[-1]['node']
                    suggestions = latest_message['suggestedReplies']
                    state = latest_message['state']
                    if state == 'complete' and suggestions:
                        break
                    if state == 'error_user_message_too_long':
                        break
                else:
                    break
            queue.put({'text': message["text"], 'response':'', 'suggestedReplies': suggestions, 'state': state, 'chatCode': chatCode, 'chatId': chatId, 'title': title})
        
        if message["state"] != "error_user_message_too_long": 
            t1 = threading.Thread(target=recv_post_thread, daemon=True)
            t1.start()
            
            if suggest_replies:
                self.suggestions_queue = queue.Queue()
                t2 = threading.Thread(target=get_suggestions, args=(self.suggestions_queue, chatCode, 5), daemon=True)
                t2.start()
                try:
                    suggestions = self.suggestions_queue.get(timeout=5)
                    yield suggestions
                except queue.Empty:
                    yield {'text': message["text"], 'response':'', 'suggestedReplies': [], 'state': None, 'chatCode': chatCode, 'chatId': chatId, 'title': title}
                del self.suggestions_queue
        
        del self.active_messages[human_message_id]
        del self.message_queues[human_message_id]
        self.retry_attempts = 3
        
    def cancel_message(self, chunk: dict):
        self.message_generating = False
        variables = {"messageId": chunk["messageId"], "textLength": len(chunk["text"]), "linkifiedTextLength": len(chunk["linkifiedText"])}
        self.send_request('gql_POST', 'ChatHelpers_messageCancel_Mutation', variables)
        
    def chat_break(self, bot: str, chatId: int=None, chatCode: str=None):
        bot = bot_map(bot)
        chatdata = self.get_threadData(bot, chatCode, chatId)
        chatId = chatdata['chatId']
        id = chatdata['id']
        variables = {"connections": [
                f"client:{id}:__ChatMessagesView_chat_messagesConnection_connection"],
                "chatId": chatId}
        self.send_request('gql_POST', 'ChatHelpers_addMessageBreakEdgeMutation_Mutation', variables)
            
    def delete_message(self, message_ids):
        variables = {'messageIds': message_ids}
        self.send_request('gql_POST', 'DeleteMessageMutation', variables)
    
    def purge_conversation(self, bot: str, chatId: int=None, chatCode: str=None, count: int=50, del_all: bool=False):
        bot = bot_map(bot)
        if chatId != None and chatCode == None:
            chatdata = self.get_threadData(bot, chatCode, chatId)
            chatCode = chatdata['chatCode']
        variables = {'chatCode': chatCode}
        response_json = self.send_request('gql_POST', 'ChatPageQuery', variables)
        if response_json['data'] == None and response_json["errors"]:
            raise RuntimeError(f"An unknown error occurred. Raw response data: {response_json}")
        edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
        
        if del_all == True:
            while True:
                if len(edges) == 0:
                    break
                message_ids = []
                for edge in edges:
                    message_ids.append(edge['node']['messageId'])
                self.delete_message(message_ids)
                sleep(0.5)
                response_json = self.send_request('gql_POST', 'ChatPageQuery', variables)
                edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
            logger.info(f"Deleted {len(message_ids)} messages of {chatCode}")
        else:
            num = count
            while True:
                if len(edges) == 0 or num == 0:
                    break
                message_ids = []
                for edge in edges:
                    message_ids.append(edge['node']['messageId'])
                self.delete_message(message_ids)
                sleep(0.5)
                num -= len(message_ids)
                if len(edges) < num:
                    response_json = self.send_request('gql_POST', 'ChatPageQuery', variables)
                    edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
            logger.info(f"Deleted {count-num} messages of {chatCode}")
            
    def purge_all_conversations(self):
        self.current_thread = {}
        self.send_request('gql_POST', 'DeleteUserMessagesMutation', {})
    
    def delete_chat(self, bot: str, chatId: any=None, chatCode: any=None, del_all: bool=False):
        bot = bot_map(bot)
        try:
            chatdata = self.get_chat_history(bot=bot)['data'][bot]
        except:
            raise RuntimeError(f"No chat found for {bot}. Make sure the bot has a chat history before deleting.")
        if chatId != None and not isinstance(chatId, list):
            if bot in self.current_thread:
                for thread in range(len(self.current_thread[bot])):
                    if self.current_thread[bot][thread]['chatId'] == chatId:
                        del self.current_thread[bot][thread]
                        break
            self.send_request('gql_POST', 'DeleteChat', {'chatId': chatId})
            logger.info(f"Chat {chatId} deleted")
        if del_all == True:
            if bot in self.current_thread:
                del self.current_thread[bot]
            for chat in chatdata:
                self.send_request('gql_POST', 'DeleteChat', {'chatId': chat['chatId']})
                logger.info(f"Chat {chat['chatId']} deleted")
        if chatCode != None:
                for chat in chatdata:
                    if isinstance(chatCode, list):
                        if chat['chatCode'] in chatCode:
                            chatId = chat['chatId']
                            if bot in self.current_thread:
                                for thread in range(len(self.current_thread[bot])):
                                    if self.current_thread[bot][thread]['chatId'] == chatId:
                                        del self.current_thread[bot][thread]
                                        break
                            self.send_request('gql_POST', 'DeleteChat', {'chatId': chatId})
                            logger.info(f"Chat {chatId} deleted")
                    else:
                        if chat['chatCode'] == chatCode:
                            chatId = chat['chatId']
                            if bot in self.current_thread:
                                for thread in range(len(self.current_thread[bot])):
                                    if self.current_thread[bot][thread]['chatId'] == chatId:
                                        del self.current_thread[bot][thread]
                                        break
                            self.send_request('gql_POST', 'DeleteChat', {'chatId': chatId})
                            logger.info(f"Chat {chatId} deleted")
                            break               
        elif chatId != None and isinstance(chatId, list):
            for chat in chatId:
                if bot in self.current_thread:
                    if self.current_thread[bot]:
                        for thread in range(len(self.current_thread[bot])):
                            if self.current_thread[bot][thread]['chatId'] == chat:
                                del self.current_thread[bot][thread]
                                break
                self.send_request('gql_POST', 'DeleteChat', {'chatId': chat})
                logger.info(f"Chat {chat} deleted")  
                
    def get_previous_messages(self, bot: str, chatId: int = None, chatCode: str = None, count: int = 50, get_all: bool = False):
        bot = bot_map(bot)
        try:
            getchatdata = self.get_threadData(bot, chatCode, chatId)
        except:
            raise RuntimeError(f"Thread not found. Make sure the thread exists before getting messages.")
        chatCode = getchatdata['chatCode']
        id = getchatdata['id']
        messages = []
        cursor = None
        edges = True

        if get_all:
            while edges:
                variables = {'count': 100, 'cursor': cursor, 'id': id}
                response_json = self.send_request('gql_POST', 'ChatListPaginationQuery', variables)
                chatdata = response_json['data']['node']
                edges = chatdata['messagesConnection']['edges'][::-1]
                for edge in edges:
                    messages.append({'author': edge['node']['author'], 'text': edge['node']['text'], 'messageId': edge['node']['messageId']})
                cursor = chatdata['messagesConnection']['pageInfo']['startCursor']
        else:
            num = count
            while edges and num > 0:
                variables = {'count': 100, 'cursor': cursor, 'id': id}
                response_json = self.send_request('gql_POST', 'ChatListPaginationQuery', variables)
                chatdata = response_json['data']['node']
                edges = chatdata['messagesConnection']['edges'][::-1]
                for edge in edges:
                    messages.append({'author': edge['node']['author'], 'text': edge['node']['text'], 'messageId': edge['node']['messageId']})
                    num -= 1
                    if len(messages) == count:
                        break
                cursor = chatdata['messagesConnection']['pageInfo']['startCursor']

        logger.info(f"Found {len(messages)} messages of {chatCode}")
        return messages[::-1]
    
    def get_user_bots(self, user: str):
        variables = {'handle': user}
        response_json = self.send_request('gql_POST', 'HandleProfilePageQuery', variables)
        if response_json['data'] == None and response_json["errors"]:
            raise RuntimeError(f"User {user} not found. Make sure the user exists before getting bots.")
        userData = response_json['data']['user']
        logger.info(f"Found {userData['createdBotCount']} bots of {user}")
        botsData = userData['createdBots']
        bots = [each['handle'] for each in botsData]
        return bots
        
    def complete_profile(self, handle: str=None):
        if handle == None:
            handle = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))
        variables = {"handle" : handle}
        self.send_request('gql_POST', 'NuxInitialModal_poeSetHandle_Mutation', variables)
        self.send_request('gql_POST', 'MarkMultiplayerNuxCompleted', {})
    
    def create_bot(self, handle, prompt, display_name=None, base_model="chinchilla", description="", intro_message="", api_key=None, api_bot=False, api_url=None, prompt_public=True, pfp_url=None, linkification=False,  markdown_rendering=True, suggested_replies=False, private=False, temperature=None):
        # Auto complete profile
        try:
            self.send_request('gql_POST', 'MarkMultiplayerNuxCompleted', {})
        except:
            self.complete_profile()
        variables = {
            "model": base_model,
            "displayName": display_name,
            "handle": handle,
            "prompt": prompt,
            "isPromptPublic": prompt_public,
            "introduction": intro_message,
            "description": description,
            "profilePictureUrl": pfp_url,
            "apiUrl": api_url,
            "apiKey": api_key,
            "isApiBot": api_bot,
            "hasLinkification": linkification,
            "hasMarkdownRendering": markdown_rendering,
            "hasSuggestedReplies": suggested_replies,
            "isPrivateBot": private,
            "temperature": temperature
        }
        result = self.send_request('gql_POST', 'PoeBotCreate', variables)['data']['poeBotCreate']
        if result["status"] != "success":
           logger.error(f"Poe returned an error while trying to create a bot: {result['status']}")
        else:
           logger.info(f"Bot created successfully | {handle}")
        
    # get_bot logic 
    def get_botData(self, handle):
        variables = {"botHandle": handle}
        try:
            response_json = self.send_request('gql_POST', 'BotLandingPageQuery', variables)
            return response_json['data']['bot']
        except Exception as e:
            raise ValueError(
                f"Fail to get botId from {handle}. Make sure the bot exists and you have access to it."
            ) from e

    def edit_bot(self, handle, prompt, display_name=None, base_model="chinchilla", description="",
                intro_message="", api_key=None, api_url=None, private=False,
                prompt_public=True, pfp_url=None, linkification=False,
                markdown_rendering=True, suggested_replies=False, temperature=None):     
        variables = {
        "baseBot": base_model,
        "botId": self.get_botData(handle)['botId'],
        "handle": handle,
        "displayName": display_name,
        "prompt": prompt,
        "isPromptPublic": prompt_public,
        "introduction": intro_message,
        "description": description,
        "profilePictureUrl": pfp_url,
        "apiUrl": api_url,
        "apiKey": api_key,
        "hasLinkification": linkification,
        "hasMarkdownRendering": markdown_rendering,
        "hasSuggestedReplies": suggested_replies,
        "isPrivateBot": private,
        "temperature": temperature
        }
        result = self.send_request('gql_POST', 'PoeBotEdit', variables)["data"]["poeBotEdit"]
        if result["status"] != "success":
            logger.error(f"Poe returned an error while trying to edit a bot: {result['status']}")
        else:
            logger.info(f"Bot edited successfully | {handle}")
      
    def delete_bot(self, handle):
        isCreator = self.get_botData(handle)['viewerIsCreator']
        botId = self.get_botData(handle)['botId']
        try:
            if isCreator == True:
                response = self.send_request('gql_POST', "BotInfoCardActionBar_poeBotDelete_Mutation", {"botId": botId})
            else:
                response = self.send_request('gql_POST',
                    "BotInfoCardActionBar_poeRemoveBotFromUserList_Mutation",
                    {"connections": [
                        "client:Vmlld2VyOjA=:__HomeBotSelector_viewer_availableBotsConnection_connection"],
                        "botId": botId}
                )
        except Exception:
            raise ValueError(
                f"Failed to delete bot {handle}. Make sure the bot exists and belongs to you."
            )
        if response["data"] is None and response["errors"]:
            raise ValueError(
                f"Failed to delete bot {handle} :{response['errors'][0]['message']}"
            )
        else:
            logger.info(f"Bot deleted successfully | {handle}")
            
    def get_available_categories(self):
        categories = []
        response_json = self.send_request('gql_POST', 'ExploreBotsIndexPageQuery', {"categoryName":"defaultCategory"})
        if response_json['data'] == None and response_json["errors"]:
            raise RuntimeError(f"An unknown error occurred. Raw response data: {response_json}")
        else:
            for category in response_json['data']['exploreBotsCategoryObjects']:
                categories.append(category['categoryName'])
        return categories
                
    def explore(self, categoryName: str='defaultCategory', search: str=None, entity_type: str = "bot", count: int = 50, explore_all: bool = False):
        if entity_type not in ["bot", "user"]:
            raise ValueError(f"Entity type {entity_type} not found. Make sure the entity type is either bot or user.")
        if categoryName != 'defaultCategory' and categoryName not in self.get_available_categories():
            raise ValueError(f"Category {categoryName} not found. Make sure the category exists before exploring.")
        bots = []
        if search == None:
            query_name = "ExploreBotsListPaginationQuery"
            variables = {"categoryName": categoryName, "count": count}
            connectionType = "exploreBotsConnection"
        else:
            query_name = "SearchResultsListPaginationQuery"
            variables = {"query": search, "entityType": entity_type, "count": 50}
            connectionType = "searchEntityConnection"
            
        result = self.send_request("gql_POST", query_name, variables)
        if search == None:
            new_cursor = result["data"][connectionType]["edges"][-1]["cursor"]
        else:
            new_cursor = 60
            
        if entity_type == "bot":
            bots += [
                each["node"]['handle'] for each in result["data"][connectionType]["edges"]
            ]
        else:
            bots += [
                each["node"]['nullableHandle'] for each in result["data"][connectionType]["edges"]
            ]
        if len(bots) >= count and not explore_all:
            if entity_type == "bot":
                logger.info("Succeed to explore bots")
            else:
                logger.info("Succeed to explore users")
            return bots[:count]
        while len(bots) < count or explore_all:
            if search == None:
                result = self.send_request("gql_POST", query_name, {"categoryName": categoryName, "count": count, "cursor": new_cursor})
            else:
                result = self.send_request("gql_POST", query_name, {"query": search, "entityType": entity_type, "count": 50, "cursor": new_cursor})
            if len(result["data"][connectionType]["edges"]) == 0:
                if not explore_all:
                    if entity_type == "bot":
                        logger.info(f"No more bots could be explored, only {len(bots)} bots found.")
                    else:
                        logger.info(f"No more users could be explored, only {len(bots)} users found.")
                return bots
            if search == None:
                new_cursor = result["data"][connectionType]["edges"][-1]["cursor"]
            else:
                new_cursor += 50
            if entity_type == "bot":
                new_bots = [
                    each["node"]['handle'] for each in result["data"][connectionType]["edges"]
                ]
            else:
                new_bots = [
                    each["node"]['nullableHandle'] for each in result["data"][connectionType]["edges"]
                ]
            bots += new_bots
        
        if entity_type == "bot":
            logger.info("Succeed to explore bots")
        else:
            logger.info("Succeed to explore users")
        return bots[:count]
    
    def share_chat(self, bot: str, chatId: int=None, chatCode: str=None, count: int=None):
        bot = bot_map(bot)
        chatdata = self.get_threadData(bot, chatCode, chatId)
        chatCode = chatdata['chatCode']
        chatId = chatdata['chatId']
        variables = {'chatCode': chatCode}
        response_json = self.send_request('gql_POST', 'ChatPageQuery', variables)
        edges = response_json['data']['chatOfCode']['messagesConnection']['edges']
        if count == None:
            count = len(edges)
        message_ids = []
        for edge in edges:
            message_ids.append(edge['node']['messageId'])
        variables = {'chatId': chatId, 'messageIds': message_ids if count == None else message_ids[:count]}
        response_json = self.send_request('gql_POST', 'ShareMessageMutation', variables)
        if response_json['data']['messagesShare']:
            shareCode = response_json['data']['messagesShare']["shareCode"]
            logger.info(f'Shared {count} messages with code: {shareCode}')
            return shareCode
        else:
            logger.error(f'An error occurred while sharing the messages')
            return None
        
    def import_chat(self, bot:str="", shareCode: str=""):
        bot = bot_map(bot)
        variables = {'botName': bot, 'shareCode': shareCode, 'postId': None}
        response_json = self.send_request('gql_POST', 'ContinueChatCTAButton_continueChatFromPoeShare_Mutation', variables)
        if response_json['data']['continueChatFromPoeShare']['status'] == 'success':
            logger.info(f'Chat imported successfully')
            chatCode = response_json['data']['continueChatFromPoeShare']['messages'][0]['node']['chat']['chatCode']
            chatdata = self.get_threadData(bot, chatCode=chatCode)
            chatId = chatdata['chatId']
            return {'chatId': chatId, 'chatCode': chatCode}
        else:
            logger.error(f'An error occurred while importing the chat')
            return None