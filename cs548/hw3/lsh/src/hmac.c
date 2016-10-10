/*
 * Copyright (c) 2016 NSR (National Security Research Institute)
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy 
 * of this software and associated documentation files (the "Software"), to deal 
 * in the Software without restriction, including without limitation the rights 
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
 * copies of the Software, and to permit persons to whom the Software is 
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in 
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
 * THE SOFTWARE.
 */

#include <string.h>
#include "../include/hmac.h"

lsh_err hmac_lsh_init(struct HMAC_LSH_Context * ctx, lsh_type algtype, const lsh_u8 * key, size_t keybytelen){
	lsh_err result;

	lsh_u8 ipad[LSH512_MSG_BLK_BYTE_LEN];
	lsh_u8 tempKey[LSH512_HASH_VAL_MAX_BYTE_LEN];

	lsh_uint i;

	lsh_uint blockbytelen;

	if (ctx == NULL){
		return LSH_ERR_NULL_PTR;
	}

	if (LSH_IS_LSH256(algtype)){
		blockbytelen = LSH256_MSG_BLK_BYTE_LEN;
	}
	else{
		blockbytelen = LSH512_MSG_BLK_BYTE_LEN;
	}

	if (keybytelen > blockbytelen){
		result = lsh_init(&ctx->hash_ctx, algtype);
		if (result != LSH_SUCCESS){
			return result;
		}

		result = lsh_update(&ctx->hash_ctx, key, keybytelen * 8);
		if (result != LSH_SUCCESS){
			return result;
		}

		result = lsh_final(&ctx->hash_ctx, tempKey);
		if (result != LSH_SUCCESS){
			return result;
		}

		key = tempKey;
		keybytelen = LSH_GET_HASHBYTE(algtype);
	}

	for (i = 0; i < keybytelen; i++){
		ipad[i] = key[i] ^ 0x36;
		ctx->opad[i] = key[i] ^ 0x5c;
	}

	for (; i < blockbytelen; i++){
		ipad[i] = 0x36;
		ctx->opad[i] = 0x5c;
	}

	result = lsh_init(&ctx->hash_ctx, algtype);
	if (result != LSH_SUCCESS){
		return result;
	}

	result = lsh_update(&ctx->hash_ctx, ipad, blockbytelen * 8);
	if (result != LSH_SUCCESS){
		return result;
	}

	memset(ipad, 0, blockbytelen);
	return LSH_SUCCESS;

}

lsh_err hmac_lsh_update(struct HMAC_LSH_Context * ctx, const lsh_u8* data, size_t databytelen){
	if (ctx == NULL || data == NULL){
		return LSH_ERR_NULL_PTR;
	}

	return lsh_update(&ctx->hash_ctx, data, databytelen * 8);
	
}

lsh_err hmac_lsh_final(struct HMAC_LSH_Context * ctx, lsh_u8* digest){

	lsh_err result;
	lsh_type algtype;
	lsh_uint blockbytelen;

	if (ctx == NULL || digest == NULL){
		return LSH_ERR_NULL_PTR;
	}

	result = lsh_final(&ctx->hash_ctx, digest);
	if (result != LSH_SUCCESS){
		return result;
	}

	algtype = ctx->hash_ctx.algtype;
	if (LSH_IS_LSH256(algtype)){
		blockbytelen = LSH256_MSG_BLK_BYTE_LEN;
	}
	else{
		blockbytelen = LSH512_MSG_BLK_BYTE_LEN;
	}
	
	result = lsh_init(&ctx->hash_ctx, algtype);
	if (result != LSH_SUCCESS){
		return result;
	}

	result = lsh_update(&ctx->hash_ctx, ctx->opad, blockbytelen*8);
	memset(ctx->opad, 0, blockbytelen);
	if (result != LSH_SUCCESS){
		return result;
	}

	result = lsh_update(&ctx->hash_ctx, digest, LSH_GET_HASHBIT(algtype));
	if (result != LSH_SUCCESS){
		return result;
	}

	return lsh_final(&ctx->hash_ctx, digest);
}

lsh_err hmac_lsh_digest(lsh_type algtype, const lsh_u8* key, size_t keylen, const lsh_u8* data, size_t databytelen, lsh_u8* digest){
	struct HMAC_LSH_Context ctx;
	int result;

	result = hmac_lsh_init(&ctx, algtype, key, keylen);
	if (result != LSH_SUCCESS){
		return result;
	}

	result = hmac_lsh_update(&ctx, data, databytelen);
	if (result != LSH_SUCCESS){
		return result;
	}

	return hmac_lsh_final(&ctx, digest);
}
