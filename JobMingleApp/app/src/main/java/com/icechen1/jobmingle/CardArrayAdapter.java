package com.icechen1.jobmingle;

import android.content.Context;
import android.graphics.Bitmap;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

/**
 * Created by Yuwei on 2015-02-21.
 */
public class CardArrayAdapter extends ArrayAdapter<String> {

    public CardArrayAdapter(Context context, int resource, List<String> objects) {
        super(context, resource, objects);
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        // Check if an existing view is being reused, otherwise inflate the view
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.card_layout, parent, false);
        }
        String word = getItem(position);
        TextView textView = (TextView) convertView.findViewById(R.id.card_textView);
        textView.setText(word);
        return convertView;
    }
}