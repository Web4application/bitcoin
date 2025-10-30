import { createClient } from 'bitcoin';
import { NextResponse } from 'next/server';

const redis = await createClient().connect();

export const POST = async () => {
  // Fetch data from Redis
  const result = await redis.get("item");
  
  // Return the result in the response
  return new NextResponse(JSON.stringify({ result }), { status: 200 });
};

#![allow(non_snake_case, clippy::large_enum_variant, clippy::enum_variant_names)]
use std::time::Duration;

use candid::{self, CandidType, Deserialize, Principal};

pub const SCRAPING_LOGS_INTERVAL: Duration = Duration::from_secs(3 * 60);

fn setup_timers() {
    // // Start scraping logs immediately after the install, then repeat with the interval.
    ic_cdk_timers::set_timer(Duration::ZERO, || ic_cdk::spawn(check_evm_log()));
    ic_cdk_timers::set_timer_interval(SCRAPING_LOGS_INTERVAL, || ic_cdk::spawn(check_evm_log()));
}

#[ic_cdk::init]
fn init() {
    // start timers upon canister initialization
    setup_timers();
}

// Function checks the logs of an ETH smart contract for an event
// If a particular event is found, it sends bitcoin to an address
async fn check_evm_log() {
    // the cycles we attach to the message to pay for the service provide by
    // the EVM RPC canister
    let cycles = 10_000_000_000;
    // This is a test canister without API keys, for production use 7hfb6-caaaa-aaaar-qadga-cai
    let canister_id =
        Principal::from_text("7hfb6-caaaa-aaaar-qadga-cai").expect("principal should be valid");
    // call the eth_getLogs function on the EVM RPC canister
    let (result,) = ic_cdk::api::call::call_with_payment128::<
        (RpcServices, Option<RpcConfig>, GetLogsArgs),
        (MultiGetLogsResult,),
    >(
        canister_id,
        "eth_getLogs",
        (
            RpcServices::EthMainnet(None),
            None,
            // for more information on eth_getLogs check
            // https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getlogs
            GetLogsArgs {
                fromBlock: Some(BlockTag::Finalized),
                toBlock: Some(BlockTag::Finalized),
                addresses: vec!["dummy_address".to_string()],
                topics: Some(vec![vec!["topic1".to_string()], vec!["topic2".to_string()]]),
            },
        ),
        cycles,
    )
    .await
    .expect("Call failed");

    match result {
        MultiGetLogsResult::Consistent(_) => send_bitcoin().await,
        MultiGetLogsResult::Inconsistent(_) => {
            panic!("RPC providers gave inconsistent results")
        }
    }
}

// Function that sends bitcoin. This is used by check_evm_log()
async fn send_bitcoin() {
    // for more information on bitcoin_send_transaction check
    // /docs/references/ic-interface-spec/#ic-bitcoin_send_transaction
    ic_cdk::api::management_canister::bitcoin::bitcoin_send_transaction(
        ic_cdk::api::management_canister::bitcoin::SendTransactionRequest {
            transaction: b"beef".into(),
            network: ic_cdk::api::management_canister::bitcoin::BitcoinNetwork::Testnet,
        },
    )
    .await
    .expect("Call failed");
}

//TYPE DECLARATIONSpush

#[derive(CandidType, Deserialize, Debug, Clone)]
pub enum EthSepoliaService {
    Alchemy,
    BlockPi,
    PublicNode,
    Ankr,
}

#[derive(CandidType, Deserialize, Debug, Clone)]
pub struct HttpHeader {
    pub value: String,
    pub name: String,
}

#[derive(CandidType, Deserialize, Debug, Clone)]
pub struct RpcApi {
    pub url: String,
    pub headers: Option<Vec<HttpHeader>>,
}

#[derive(CandidType, Deserialize, Debug, Clone)]
pub enum EthMainnetService {
    Alchemy,
    BlockPi,
    Cloudflare,
    PublicNode,
    Ankr,
}

#[derive(CandidType, Deserialize, Debug, Clone)]
pub enum RpcServices {
    EthSepolia(Option<Vec<EthSepoliaService>>),
    Custom { chainId: u64, services: Vec<RpcApi> },
    EthMainnet(Option<Vec<EthMainnetService>>),
}

#[derive(CandidType, Deserialize)]
pub struct RpcConfig {
    pub responseSizeEstimate: Option<u64>,
}

#[derive(CandidType, Deserialize, Debug, Clone)]
pub enum BlockTag {
    Earliest,
    Safe,
    Finalized,
    Latest,
    Number(candid::Nat),
    Pending,
}

#[derive(CandidType, Deserialize, Debug)]
pub struct JsonRpcError {
    pub code: i64,
    pub message: String,
}

#[derive(CandidType, Deserialize, Debug)]
pub enum ProviderError {
    TooFewCycles {
        expected: candid::Nat,
        received: candid::Nat,
    },
    MissingRequiredProvider,
    ProviderNotFound,
    NoPermission,
}

#[derive(CandidType, Deserialize, Debug)]
pub enum ValidationError {
    CredentialPathNotAllowed,
    HostNotAllowed(String),
    CredentialHeaderNotAllowed,
    UrlParseError(String),
    Custom(String),
    InvalidHex(String),
}

#[derive(CandidType, Deserialize, Debug, PartialEq)]
pub enum RejectionCode {
    NoError,
    CanisterError,
    SysTransient,
    DestinationInvalid,
    Unknown,
    SysFatal,
    CanisterReject,
}

#[derive(CandidType, Deserialize, Debug)]
pub enum HttpOutcallError {
    IcError {
        code: RejectionCode,
        message: String,
    },
    InvalidHttpJsonRpcResponse {
        status: u16,
        body: String,
        parsingError: Option<String>,
    },
}

#[derive(CandidType, Deserialize, Debug)]
pub enum RpcError {
    JsonRpcError(JsonRpcError),
    ProviderError(ProviderError),
    ValidationError(ValidationError),
    HttpOutcallError(HttpOutcallError),
}

#[derive(CandidType, Deserialize)]
pub enum RpcService {
    EthSepolia(EthSepoliaService),
    Custom(RpcApi),
    EthMainnet(EthMainnetService),
    Chain(u64),
    Provider(u64),
}

#[derive(CandidType, Deserialize)]
pub struct GetLogsArgs {
    pub fromBlock: Option<BlockTag>,
    pub toBlock: Option<BlockTag>,
    pub addresses: Vec<String>,
    pub topics: Option<Vec<Vec<String>>>,
}

#[derive(CandidType, Deserialize, Debug, Clone, PartialEq)]
pub struct LogEntry {
    pub transactionHash: Option<String>,
    pub blockNumber: Option<candid::Nat>,
    pub data: String,
    pub blockHash: Option<String>,
    pub transactionIndex: Option<candid::Nat>,
    pub topics: Vec<String>,
    pub address: String,
    pub logIndex: Option<candid::Nat>,
    pub removed: bool,
}

#[derive(CandidType, Deserialize)]
pub enum GetLogsResult {
    Ok(Vec<LogEntry>),
    Err(RpcError),
}

#[derive(CandidType, Deserialize)]
pub enum MultiGetLogsResult {
    Consistent(GetLogsResult),
    Inconsistent(Vec<(RpcService, GetLogsResult)>),
}
